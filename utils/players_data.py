import os
from typing import Dict, List

import pandas as pd
import requests

api_key = os.getenv("API_FOOTBALL_KEY")
HEADERS = {
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
    "X-RapidAPI-Key": api_key,
}
LEAGUES_URL = "https://api-football-v1.p.rapidapi.com/v3/leagues"
TEAMS_URL = "https://api-football-v1.p.rapidapi.com/v3/teams"
PLAYERS_URL = "https://api-football-v1.p.rapidapi.com/v3/players"

FAVORITE_LEAGUES = {
    "Premier League": 39,
    "La Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78,
    "Ligue 1": 61,
    "Eredivisie": 88,
    "UEFA Champions League": 2,
    "UEFA Europa League": 3,
    "UEFA Conference League": 4,
    "UEFA Super Cup": 5,
    "Championship": 180,
    "Primeira Liga": 94,
}


def get_all_leagues() -> List[Dict]:
    """Call it to get all available leagues"""
    response = requests.get(LEAGUES_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error fetching leagues: {response.status_code}")
        return []
    data = response.json()
    leagues = [
        {
            "league_id": league["league"]["id"],
            "league_name": league["league"]["name"],
        }
        for league in data["response"]
    ]
    return leagues


def get_teams_from_league(
    league_id: int, league_name: str, season: int = 2024
) -> pd.DataFrame:
    """Get all teams playing in a given league"""
    params = {"league": league_id, "season": season}
    response = requests.get(TEAMS_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error fetching teams for league {league_id}: {response.status_code}")
        return []
    data = response.json()
    teams = [
        {
            "Team ID": team_info["team"]["id"],
            "Team": team_info["team"]["name"],
            "League": league_name,
        }
        for team_info in data["response"]
    ]
    print(f"Fetched {len(teams)} teams for league: {league_name}")
    return pd.DataFrame(teams)


def get_all_teams(leagues_dict: Dict[str, int] = FAVORITE_LEAGUES) -> pd.DataFrame:
    """Get all teams from a list of leagues and save them to a CSV file"""
    all_teams = []
    for (
        league_name,
        league_id,
    ) in leagues_dict.items():
        print(f"Fetching teams for league: {league_name} (ID: {league_id})")
        league_teams = get_teams_from_league(int(league_id), league_name)
        if len(league_teams) < 10:
            continue
        all_teams.append(league_teams)
    all_teams_df = pd.concat(all_teams)
    all_teams_df.to_csv("teams.csv", index=False)


def get_player_id(team_id: int, player_name: str, season: int) -> int:
    params = {
        "search": player_name,
        "team": team_id,
        "season": season,
    }
    response = requests.get(PLAYERS_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error fetching player data: {response.status_code}")
        return None
    data = response.json()

    # Extract Player ID
    if not data["response"]:
        print(f"No player found with name '{player_name}' in team ID {team_id}")
        return None
    player = data["response"][0]  # Assume the first match is the desired player
    player_id = player["player"]["id"]
    print(f"Found player: {player['player']['name']} (ID: {player_id})")
    return player_id


def get_player_stats(player_id: int, team_id: int, season=2024) -> pd.DataFrame:
    params = {"id": player_id, "team": team_id, "season": season}
    response = requests.get(PLAYERS_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error fetching player stats: {response.status_code}")
        return None
    data = response.json()
    if not data["response"]:
        print(f"No stats found for player ID {player_id} in team ID {team_id}")
        return None
    return _parse_player_data(data)


def _parse_player_data(data: Dict) -> pd.DataFrame:
    player_info = data["response"][0]["player"]
    player_name = player_info["name"]
    age = player_info["age"]
    nationality = player_info["nationality"]
    weight = player_info["weight"]
    height = player_info["height"]
    stats = data["response"][0]["statistics"]
    # Parse stats into a DataFrame
    rows = []
    for stat in stats:
        rows.append(
            {
                "Player Name": player_name,
                "Age": age,
                "Nationality": nationality,
                "Weight": weight,
                "Height": height,
                "League": stat["league"]["name"],
                "Team": stat["team"]["name"],
                "Appearances": stat["games"]["appearences"],
                "Lineups": stat["games"]["lineups"],
                "Minutes": stat["games"]["minutes"],
                "Goals": stat["goals"]["total"],
                "Assists": stat["goals"]["assists"],
                "Yellow Cards": stat["cards"]["yellow"],
                "Red Cards": stat["cards"]["red"],
                "Rating": stat["games"]["rating"],
                "Passes Total": stat["passes"]["total"],
                "Tackles Total": stat["tackles"]["total"],
                "Duels Total": stat["duels"]["total"],
            }
        )
    player_df = pd.DataFrame(rows)
    return player_df


def get_team_id(team_name: str, all_teams_path: str = "all_teams.csv") -> int:
    all_teams = pd.read_csv(all_teams_path)
    team_id = all_teams.loc[all_teams["Team"] == team_name]["Team ID"].values
    return team_id[0] if len(team_id) > 0 else None


def get_player_data(
    player_name: str, team_name: str, season: int = 2024
) -> pd.DataFrame:
    """Get player stats using player name and his current team"""
    team_id = get_team_id(team_name)
    if not team_id:
        print(f"Team '{team_name}' not found")
        return None
    player_id = get_player_id(team_id, player_name, season)
    if player_id is None:
        return None
    player_stats = get_player_stats(player_id, team_id, season)
    return player_stats
