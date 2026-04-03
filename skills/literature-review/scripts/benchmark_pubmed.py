import sys
import time
import asyncio
import unittest.mock as mock
from pathlib import Path

# Mock requests and aiohttp before they're imported
mock_requests = mock.MagicMock()
sys.modules["requests"] = mock_requests

mock_aiohttp = mock.MagicMock()
sys.modules["aiohttp"] = mock_aiohttp

# Add the script directory to sys.path
script_dir = Path("skills/literature-review/scripts")
sys.path.append(str(script_dir))

import fetch_pubmed

def run_benchmark():
    # Mock data
    mock_id_list = [str(i) for i in range(1000)]
    mock_search_result = {
        "esearchresult": {
            "idlist": mock_id_list,
            "count": "1000"
        }
    }

    def get_mock_summary(ids):
        result = {}
        for pmid in ids.split(","):
            result[pmid] = {
                "authors": [{"name": f"Author {pmid}"}],
                "title": f"Title {pmid}",
                "pubdate": "2023",
                "fulljournalname": "Journal",
                "source": "Source",
                "elocationid": f"doi:10.1234/{pmid}"
            }
        return {"result": result}

    # Mock aiohttp
    class MockAsyncResponse:
        def __init__(self, json_data):
            self.json_data = json_data
        async def __aenter__(self):
            # Simulate network latency
            await asyncio.sleep(0.1)
            return self
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
        async def json(self):
            return self.json_data
        def raise_for_status(self):
            pass

    class MockClientSession:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
        def get(self, url, params=None, **kwargs):
            if "esearch.fcgi" in url:
                return MockAsyncResponse(mock_search_result)
            elif "esummary.fcgi" in url:
                return MockAsyncResponse(get_mock_summary(params.get("id", "")))
            return MockAsyncResponse({})

    mock_aiohttp.ClientSession = MockClientSession

    print("Starting async benchmark (1000 results, 5 batches)...")
    start_time = time.time()
    # Use the synchronous wrapper
    result = fetch_pubmed.fetch_pubmed("test query", 1000, None, None, "test-tool")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Async execution time: {duration:.4f} seconds")
    print(f"Results returned: {result.get('returned')}")
    return duration

if __name__ == "__main__":
    run_benchmark()
