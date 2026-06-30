import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Any, List

from backend.core.config import settings
from backend.core.cache import ttl_cache
from backend.core.exceptions import CricbuzzClientError, CricbuzzAPIError
from backend.schemas.cricbuzz import LiveMatch, MatchInfo
from backend.parsers.live_matches import parse_live_matches
from backend.parsers.match_info import parse_match_info
import logging

logger = logging.getLogger(__name__)

class CricbuzzClient:
    def __init__(self):
        self.base_url = settings.cricbuzz_base_url
        self.timeout = settings.request_timeout_seconds
        
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _build_headers(self) -> Dict[str, str]:
        return {
            "x-rapidapi-key": settings.rapidapi_key or "",
            "x-rapidapi-host": settings.cricbuzz_host,
        }

    def _make_request(self, endpoint: str, method: str = "GET") -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        headers = self._build_headers()
        try:
            response = self.session.request(method, url, headers=headers, timeout=self.timeout)
            self._validate_response(response)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while making request to {endpoint}: {e}")
            raise CricbuzzClientError(f"Network error: {e}")

    def _validate_response(self, response: requests.Response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise CricbuzzAPIError(f"API Error: {e.response.status_code}")

    @ttl_cache()
    def get_live_matches(self) -> List[LiveMatch]:
        logger.info("Fetching live matches from Cricbuzz API")
        response = self._make_request("/matches/v1/live")
        data = response.json()
        return parse_live_matches(data)

    @ttl_cache()
    def get_match_info(self, match_id: int) -> MatchInfo:
        logger.info(f"Fetching match info for match {match_id}")
        response = self._make_request(f"/mcenter/v1/{match_id}")
        data = response.json()
        return parse_match_info(data)
