import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"

HEADERS ={
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

def get_live_matches():
    try: 

        url = f"{BASE_URL}/matches/v1/live"
        response = requests.get(url, headers=HEADERS, timeout = 10)
        response.raise_for_status()
        data = response.json()

        live_matches = []

        for match_type in data["typeMatches"]:
            for series in match_type["seriesMatches"]:
                if "seriesAdWrapper" in series:
                    for match in series["seriesAdWrapper"]["matches"]:
                        matchId = match["matchInfo"]["matchId"]
                        matchDesc = match["matchInfo"]["matchDesc"]
                        team1 = match["matchInfo"]["team1"]["teamName"]
                        team2 = match["matchInfo"]["team2"]["teamName"]
                        status = match["matchInfo"]["status"]
                        live_matches.append({
                            "match_Id": matchId,
                            "match_Desc": matchDesc,
                            "team1": team1,
                            "team2": team2,
                            "status": status
                        })

        return live_matches
    except requests.exceptions.RequestException as e:
        print(f"Error : {e}")
        return []


