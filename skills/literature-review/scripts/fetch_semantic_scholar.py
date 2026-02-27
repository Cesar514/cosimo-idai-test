#!/usr/bin/env python3
"""Fetch Semantic Scholar search results with caching and rate limiting."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests

API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "title,authors,year,abstract,venue,doi,url,citationCount,isOpenAccess,publicationTypes,externalIds"


def _cache_path(cache_dir: Path, key: str) -> Path:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return cache_dir / f"semanticscholar_{digest}.json"


def fetch_semantic_scholar(query: str, limit: int, api_key: str | None) -> dict[str, Any]:
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    results = []
    offset = 0
    page_size = min(100, limit)
    delay = 1.0 if api_key else 2.0

    while offset < limit:
        params = {
            "query": query,
            "limit": min(page_size, limit - offset),
            "offset": offset,
            "fields": FIELDS,
        }
        url = f"{API_URL}?{urlencode(params)}"
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("data", []))
        if not data.get("next"):
            break
        offset += page_size
        time.sleep(delay)

    return {
        "query": query,
        "returned": len(results),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Semantic Scholar records with caching.")
    parser.add_argument("--query", required=True, help="Search query string")
    parser.add_argument("--limit", type=int, default=100, help="Max results to return")
    parser.add_argument("--api-key", default=os.getenv("SEMANTIC_SCHOLAR_API_KEY"), help="Semantic Scholar API key")
    parser.add_argument("--cache-dir", default=".cache/literature-review", help="Cache directory")
    parser.add_argument("--refresh", action="store_true", help="Bypass cache")
    parser.add_argument("--output", default="semantic_scholar_results.json", help="Output JSON file")
    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_key = f"{args.query}|{args.limit}|semantic_scholar"
    cache_path = _cache_path(cache_dir, cache_key)

    if cache_path.exists() and not args.refresh:
        data = json.loads(cache_path.read_text())
    else:
        data = fetch_semantic_scholar(args.query, args.limit, args.api_key)
        cache_path.write_text(json.dumps(data, indent=2))

    Path(args.output).write_text(json.dumps(data, indent=2))
    print(f"Saved {len(data.get('results', []))} records to {args.output}")


if __name__ == "__main__":
    main()
