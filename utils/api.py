import requests

from backend.core.cache import ttl_cache
from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger(__name__)

BASE_URL = settings.cricbuzz_base_url
HEADERS = {
    "x-rapidapi-key": settings.rapidapi_key or "",
    "x-rapidapi-host": settings.cricbuzz_host,
}


def _get_json(endpoint: str) -> dict:
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS, timeout=settings.request_timeout_seconds)
    response.raise_for_status()
    return response.json()


@ttl_cache()
def get_live_matches():
    try:
        data = _get_json("/matches/v1/live")
        live_matches = []

        for match_type in data.get("typeMatches", []):
            for series in match_type.get("seriesMatches", []):
                series_wrapper = series.get("seriesAdWrapper")
                if not series_wrapper:
                    continue

                for match in series_wrapper.get("matches", []):
                    match_info = match.get("matchInfo", {})
                    team1 = match_info.get("team1", {})
                    team2 = match_info.get("team2", {})

                    live_matches.append(
                        {
                            "match_Id": match_info.get("matchId"),
                            "match_Desc": match_info.get("matchDesc", ""),
                            "team1": team1.get("teamName", "Unknown Team"),
                            "team2": team2.get("teamName", "Unknown Team"),
                            "status": match_info.get("status", "Status unavailable"),
                        }
                    )

        return live_matches
    except requests.exceptions.RequestException as exc:
        logger.exception("Unable to fetch live matches: %s", exc)
        return []


@ttl_cache()
def get_match_info(match_id):
    try:
        data = _get_json(f"/mcenter/v1/{match_id}")
        team1 = data.get("team1", {})
        team2 = data.get("team2", {})
        venue = data.get("venueinfo", {})

        return {
            "seriesname": data.get("seriesname", ""),
            "matchdesc": data.get("matchdesc", ""),
            "matchformat": data.get("matchformat", ""),
            "status": data.get("status", ""),
            "state": data.get("state", ""),
            "team1": team1.get("teamname", "Unknown Team"),
            "team2": team2.get("teamname", "Unknown Team"),
            "venue": venue.get("ground", ""),
            "city": venue.get("city", ""),
        }
    except requests.exceptions.RequestException as exc:
        logger.exception("Unable to fetch match details for %s: %s", match_id, exc)
        return {}


@ttl_cache()
def get_scorecard(match_id):
    try:
        data = _get_json(f"/mcenter/v1/{match_id}/hscard")
        return data.get("scorecard", [])
    except requests.exceptions.RequestException as exc:
        logger.exception("Unable to fetch scorecard for %s: %s", match_id, exc)
        return []
