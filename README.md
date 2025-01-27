# Football Stats Fetcher

## Overview
Football Stats Fetcher is a Python-based project that makes it easy to retrieve real-time football data and player statistics using the API-FOOTBALL service. Whether you're a football fan, a data enthusiast, or working on a sports analytics project, this tool will help you access accurate and up-to-date data effortlessly. I also plan to add more features in the future.

## Features
- Fetch data for leagues, teams, and players.
- Save league and team information to CSV files for easy reference.
- Retrieve player stats for your favorite players by name and team.

## Prerequisites
- Python 3.8+
- API-FOOTBALL account and API key (sign up [here](https://www.api-football.com/))
- Required Python libraries: `requests`, `pandas`

## Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Replace `YOUR_API_KEY` in the code with your API-FOOTBALL key.

## Usage
### Fetch League Data
Use the `get_all_leagues` function to retrieve a list of all available leagues and their IDs.
```python
leagues = get_all_leagues()
print(leagues.head(10))
```

### Save Teams to CSV
Save information about teams from your favorite leagues into a CSV file.
```python
FAVORITE_LEAGUES = {
    "Premier League": 39,
    "La Liga": 140,
    "Serie A": 135
}
get_all_teams(FAVORITE_LEAGUES)
```

### Fetch Player Stats
Retrieve stats for a specific player by providing their name and team.
```python
player_name = "Ricardo Esgaio"
team_name = "Sporting CP"
player_stats = get_player_data(player_name, team_name)
print(player_stats)
```

## Example Output
Here’s an example of the fetched stats for Ricardo Esgaio:
![image](https://github.com/user-attachments/assets/b93508ce-1dfe-4f54-a8f7-ac5d9666c34e)

## Customization
Feel free to modify the code to:
- Add more endpoints (e.g., fixtures, odds).
- Enhance the CSV exports with additional columns.
- Automate the fetching process for bulk queries.


---
Happy coding and enjoy exploring football stats!
