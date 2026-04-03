#!/usr/bin/env python3
"""Fetch PubMed records via NCBI E-utilities with caching and rate limiting."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import aiohttp

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def _cache_path(cache_dir: Path, key: str) -> Path:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return cache_dir / f"pubmed_{digest}.json"


async def fetch_batch(
    session: aiohttp.ClientSession,
    batch: list[str],
    api_key: str | None,
    email: str | None,
    tool: str,
    semaphore: asyncio.Semaphore,
    delay: float,
) -> dict[str, Any]:
    async with semaphore:
        summary_params = {
            "db": "pubmed",
            "id": ",".join(batch),
            "retmode": "json",
            "tool": tool,
        }
        if api_key:
            summary_params["api_key"] = api_key
        if email:
            summary_params["email"] = email

        async with session.get(ESUMMARY_URL, params=summary_params, timeout=30) as response:
            response.raise_for_status()
            data = await response.json()
            # Respect rate limit after request
            await asyncio.sleep(delay)
            return data.get("result", {})


async def fetch_pubmed_async(
    query: str, max_results: int, api_key: str | None, email: str | None, tool: str
) -> dict[str, Any]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance",
        "tool": tool,
    }
    if api_key:
        params["api_key"] = api_key
    if email:
        params["email"] = email

    # NCBI allows 3 requests/sec without API key, 10 with it.
    # We use a semaphore to limit concurrent requests and a sleep to maintain the rate.
    rate_limit = 10 if api_key else 3
    delay = 1.0 / rate_limit
    semaphore = asyncio.Semaphore(rate_limit)

    async with aiohttp.ClientSession() as session:
        async with session.get(ESEARCH_URL, params=params, timeout=30) as response:
            response.raise_for_status()
            search_data = await response.json()

        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return {
                "query": query,
                "count": int(search_data.get("esearchresult", {}).get("count", 0)),
                "returned": 0,
                "results": [],
            }

        batch_size = 200
        tasks = []
        for i in range(0, len(id_list), batch_size):
            batch = id_list[i : i + batch_size]
            tasks.append(fetch_batch(session, batch, api_key, email, tool, semaphore, delay))

        summaries = await asyncio.gather(*tasks)

        results = []
        # Combine summaries in original order
        for i, (summary_data) in enumerate(summaries):
            batch_start = i * batch_size
            batch_end = (i + 1) * batch_size
            batch = id_list[batch_start:batch_end]
            for pmid in batch:
                item = summary_data.get(pmid)
                if not item:
                    continue
                authors = [a.get("name") for a in item.get("authors", []) if a.get("name")]
                doi = None
                for eloc in item.get("elocationid", "").split(" "):
                    if eloc.lower().startswith("doi:"):
                        doi = eloc.split(":", 1)[1]
                        break
                results.append(
                    {
                        "pmid": pmid,
                        "title": item.get("title"),
                        "authors": authors,
                        "pubdate": item.get("pubdate"),
                        "journal": item.get("fulljournalname"),
                        "source": item.get("source"),
                        "doi": doi,
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    }
                )

        return {
            "query": query,
            "count": int(search_data.get("esearchresult", {}).get("count", 0)),
            "returned": len(results),
            "results": results,
        }


def fetch_pubmed(query: str, max_results: int, api_key: str | None, email: str | None, tool: str) -> dict[str, Any]:
    """Synchronous wrapper for fetch_pubmed_async."""
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(fetch_pubmed_async(query, max_results, api_key, email, tool))
    except RuntimeError:
        pass

    return asyncio.run(fetch_pubmed_async(query, max_results, api_key, email, tool))


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch PubMed records with caching.")
    parser.add_argument("--query", required=True, help="Search query string")
    parser.add_argument("--max-results", type=int, default=100, help="Max results to return")
    parser.add_argument("--api-key", default=os.getenv("NCBI_API_KEY"), help="NCBI API key")
    parser.add_argument("--email", default=os.getenv("NCBI_EMAIL"), help="Contact email for NCBI")
    parser.add_argument("--tool", default="literature-review-script", help="Tool name for NCBI")
    parser.add_argument("--cache-dir", default=".cache/literature-review", help="Cache directory")
    parser.add_argument("--refresh", action="store_true", help="Bypass cache")
    parser.add_argument("--output", default="pubmed_results.json", help="Output JSON file")
    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_key = f"{args.query}|{args.max_results}|pubmed"
    cache_path = _cache_path(cache_dir, cache_key)

    if cache_path.exists() and not args.refresh:
        data = json.loads(cache_path.read_text())
    else:
        data = fetch_pubmed(args.query, args.max_results, args.api_key, args.email, args.tool)
        cache_path.write_text(json.dumps(data, indent=2))

    Path(args.output).write_text(json.dumps(data, indent=2))
    print(f"Saved {len(data.get('results', []))} records to {args.output}")


if __name__ == "__main__":
    main()
