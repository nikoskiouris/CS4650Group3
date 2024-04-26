import requests
from datetime import datetime, timedelta

def get_braves_runs(start_date, end_date, api_key):
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=144&startDate={start_date}&endDate={end_date}"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "statsapi.mlb.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        total_runs = 0
        games = []
        for date in data["dates"]:
            for game in date["games"]:
                game_date = datetime.strptime(game["officialDate"], "%Y-%m-%d")
                away_team_runs = game["teams"]["away"]["score"]
                home_team_runs = game["teams"]["home"]["score"]
                game_data = {
                    "date": game_date,
                    "home_team_id": game["teams"]["home"]["team"]["id"],
                    "away_team_id": game["teams"]["away"]["team"]["id"],
                    "home_team_runs": home_team_runs,
                    "away_team_runs": away_team_runs
                }
                games.append(game_data)
                if game["teams"]["away"]["team"]["id"] == 144:
                    print(f"Date: {game_date.strftime('%Y-%m-%d')}, Braves (Away) Runs: {away_team_runs}")
                    total_runs += away_team_runs
                elif game["teams"]["home"]["team"]["id"] == 144:
                    print(f"Date: {game_date.strftime('%Y-%m-%d')}, Braves (Home) Runs: {home_team_runs}")
                    total_runs += home_team_runs
        print(f"\nTotal Runs Scored by the Braves: {total_runs}")
        return games, total_runs
    else:
        print("Failed to retrieve data from the API.")
        return [], 0
        

def get_next_game_runs(end_date, api_key):
    next_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    
    while True:
        next_date_str = next_date.strftime("%Y-%m-%d")
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=144&startDate={next_date_str}&endDate={next_date_str}"
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "statsapi.mlb.com"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data["dates"]:
                game = data["dates"][0]["games"][0]
                away_team_runs = game["teams"]["away"]["score"]
                home_team_runs = game["teams"]["home"]["score"]
                if game["teams"]["away"]["team"]["id"] == 144:
                    return away_team_runs, next_date_str
                elif game["teams"]["home"]["team"]["id"] == 144:
                    return home_team_runs, next_date_str
            else:
                next_date += timedelta(days=1)
        else:
            print("Failed to retrieve data from the API.")
            return None, None