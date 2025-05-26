import requests
import json
from datetime import datetime
from config import ODDS_API_KEY

class OddsAPI:
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.requests_remaining = None
        
    def get_remaining_requests(self):
        """Get number of remaining API requests"""
        if self.requests_remaining is None:
            # Make a test request to get the remaining count
            self.get_sports()
        return self.requests_remaining
    
    def get_sports(self):
        """Get list of available sports"""
        endpoint = f"{self.BASE_URL}/sports"
        params = {'apiKey': self.api_key}
        response = requests.get(endpoint, params=params)
        self.requests_remaining = int(response.headers.get('x-requests-remaining', 0))
        return self._handle_response(response)
    
    def get_odds(self, sport_key, regions='us', markets='h2h,spreads,totals', odds_format='american'):
        """Get odds for a specific sport with specified markets"""
        endpoint = f"{self.BASE_URL}/sports/{sport_key}/odds"
        params = {
            'apiKey': self.api_key,
            'regions': regions,
            'markets': markets,
            'oddsFormat': odds_format
        }
        response = requests.get(endpoint, params=params)
        self.requests_remaining = int(response.headers.get('x-requests-remaining', 0))
        return self._handle_response(response)
    
    def _handle_response(self, response):
        """Handle API response and format JSON output"""
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"

def format_odds_data(data):
    """Format odds data for each game with best and worst odds for each market"""
    for game in data:
        # Print game title and time
        print(f"\n{game['home_team']} vs {game['away_team']}")
        print(f"Game Time: {game['commence_time']}")
        print("-" * 50)
        
        # Process each market type
        for market_type in ['h2h', 'spreads', 'totals']:
            print(f"\n{market_type.upper()} Odds:")
            
            # Collect all odds for each team/market
            odds_data = {}
            for bookmaker in game['bookmakers']:
                for market in bookmaker['markets']:
                    if market['key'] == market_type:
                        for outcome in market['outcomes']:
                            team = outcome['name']
                            if team not in odds_data:
                                odds_data[team] = []
                            
                            # For spreads and totals, include the point value
                            if market_type in ['spreads', 'totals']:
                                odds_data[team].append({
                                    'odds': outcome['price'],
                                    'points': outcome.get('point', 'N/A'),
                                    'bookmaker': bookmaker['title']
                                })
                            else:
                                odds_data[team].append({
                                    'odds': outcome['price'],
                                    'bookmaker': bookmaker['title']
                                })
            
            # Print best and worst odds for each team
            for team, odds_list in odds_data.items():
                if odds_list:
                    best_odds = max(odds_list, key=lambda x: x['odds'])
                    worst_odds = min(odds_list, key=lambda x: x['odds'])
                    print(f"{team}:")
                    if market_type in ['spreads', 'totals']:
                        print(f"  Best: {best_odds['points']} ({best_odds['odds']}) at {best_odds['bookmaker']}")
                        print(f"  Worst: {worst_odds['points']} ({worst_odds['odds']}) at {worst_odds['bookmaker']}")
                    else:
                        print(f"  Best: {best_odds['odds']} at {best_odds['bookmaker']}")
                        print(f"  Worst: {worst_odds['odds']} at {worst_odds['bookmaker']}")

if __name__ == "__main__":
    # Initialize the API client
    api = OddsAPI(ODDS_API_KEY)
    
    # Get NBA odds
    data = api.get_odds('basketball_nba')
    print(json.dumps(data, indent=2))