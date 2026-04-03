import unittest
import unittest.mock as mock
import asyncio
import sys
from pathlib import Path

# Mock aiohttp and requests
mock_requests = mock.MagicMock()
sys.modules["requests"] = mock_requests
mock_aiohttp = mock.MagicMock()
sys.modules["aiohttp"] = mock_aiohttp

script_dir = Path("skills/literature-review/scripts")
sys.path.append(str(script_dir))

import fetch_pubmed

class TestFetchPubmed(unittest.TestCase):
    def setUp(self):
        self.mock_search_result = {
            "esearchresult": {
                "idlist": ["1", "2"],
                "count": "2"
            }
        }
        self.mock_summary_result = {
            "result": {
                "1": {"title": "Title 1", "authors": [{"name": "Author 1"}], "pubdate": "2021", "fulljournalname": "J1", "source": "S1", "elocationid": "doi:10.1/1"},
                "2": {"title": "Title 2", "authors": [{"name": "Author 2"}], "pubdate": "2022", "fulljournalname": "J2", "source": "S2", "elocationid": "doi:10.2/2"}
            }
        }

    @mock.patch("fetch_pubmed.aiohttp.ClientSession")
    def test_fetch_pubmed_success(self, mock_session_cls):
        # Mock aiohttp
        mock_session = mock_session_cls.return_value
        mock_session.__aenter__.return_value = mock_session

        class MockAsyncResponse:
            def __init__(self, json_data):
                self.json_data = json_data
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
            async def json(self): return self.json_data
            def raise_for_status(self): pass

        def get_side_effect(url, params=None, **kwargs):
            if "esearch.fcgi" in url:
                return MockAsyncResponse(self.mock_search_result)
            return MockAsyncResponse(self.mock_summary_result)

        mock_session.get.side_effect = get_side_effect

        result = fetch_pubmed.fetch_pubmed("query", 2, None, None, "tool")

        self.assertEqual(result["returned"], 2)
        self.assertEqual(result["results"][0]["pmid"], "1")
        self.assertEqual(result["results"][1]["pmid"], "2")
        self.assertEqual(result["results"][0]["doi"], "10.1/1")

if __name__ == "__main__":
    unittest.main()
