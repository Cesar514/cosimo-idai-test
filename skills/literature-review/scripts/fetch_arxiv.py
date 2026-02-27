#!/usr/bin/env python3
"""Fetch arXiv records via the public API with caching and rate limiting."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests
import xml.etree.ElementTree as ET

ARXIV_API = "http://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}


def _cache_path(cache_dir: Path, key: str) -> Path:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return cache_dir / f"arxiv_{digest}.json"


def _parse_feed(xml_text: str) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_text)
    entries = []
    for entry in root.findall("atom:entry", NS):
        title = (entry.findtext("atom:title", default="", namespaces=NS) or "").strip()
        summary = (entry.findtext("atom:summary", default="", namespaces=NS) or "").strip()
        published = entry.findtext("atom:published", default="", namespaces=NS)
        updated = entry.findtext("atom:updated", default="", namespaces=NS)
        authors = [a.findtext("atom:name", default="", namespaces=NS) for a in entry.findall("atom:author", NS)]
        doi = None
        for link in entry.findall("atom:link", NS):
            if link.attrib.get("title") == "doi":
                doi = link.attrib.get("href")
        arxiv_id = entry.findtext("atom:id", default="", namespaces=NS)
        entries.append(
            {
                "id": arxiv_id,
                "title": title,
                "summary": summary,
                "authors": [a for a in authors if a],
                "published": published,
                "updated": updated,
                "doi": doi,
                "url": arxiv_id,
            }
        )
    return entries


def fetch_arxiv(query: str, max_results: int, sort_by: str) -> dict[str, Any]:
    results = []
    batch_size = 100
    for start in range(0, max_results, batch_size):
        params = {
            "search_query": query,
            "start": start,
            "max_results": min(batch_size, max_results - start),
            "sortBy": sort_by,
        }
        url = f"{ARXIV_API}?{urlencode(params)}"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        results.extend(_parse_feed(resp.text))
        time.sleep(3)

    return {
        "query": query,
        "returned": len(results),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch arXiv records with caching.")
    parser.add_argument("--query", required=True, help="Search query string")
    parser.add_argument("--max-results", type=int, default=100, help="Max results to return")
    parser.add_argument("--sort-by", default="relevance", choices=["relevance", "lastUpdatedDate", "submittedDate"], help="Sort order")
    parser.add_argument("--cache-dir", default=".cache/literature-review", help="Cache directory")
    parser.add_argument("--refresh", action="store_true", help="Bypass cache")
    parser.add_argument("--output", default="arxiv_results.json", help="Output JSON file")
    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_key = f"{args.query}|{args.max_results}|{args.sort_by}|arxiv"
    cache_path = _cache_path(cache_dir, cache_key)

    if cache_path.exists() and not args.refresh:
        data = json.loads(cache_path.read_text())
    else:
        data = fetch_arxiv(args.query, args.max_results, args.sort_by)
        cache_path.write_text(json.dumps(data, indent=2))

    Path(args.output).write_text(json.dumps(data, indent=2))
    print(f"Saved {len(data.get('results', []))} records to {args.output}")


if __name__ == "__main__":
    main()
