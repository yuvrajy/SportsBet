# Sports Betting Odds API

A Python application that fetches and displays sports betting odds from The Odds API. Currently focused on NBA games, displaying moneyline (h2h), spreads, and totals odds from various bookmakers.

## Features

- Fetches NBA odds from multiple bookmakers
- Displays best and worst odds for each market type
- Shows game times and team matchups
- Supports moneyline (h2h), spreads, and totals markets

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sports-betting-odds.git
cd sports-betting-odds
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `config.py` file with your API key:
```python
ODDS_API_KEY = "your_api_key_here"
```

## Usage

Run the main script:
```bash
python odds_api.py
```

## API Reference

This project uses [The Odds API](https://the-odds-api.com/). You'll need to sign up for an API key to use this application.

## License

MIT License
