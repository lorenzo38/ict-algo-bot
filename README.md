# ICT Algo Hybrid Bot - Phase 1

A rule-based, statistically-driven trading bot for XAU/GBP swing trading.

## Setup

1. Install MetaTrader 5
2. Configure your demo account
3. Install dependencies: `pip install -r requirements.txt`
4. Update `config/settings.py` with your credentials and API keys
5. Run: `python main.py`

## Features

- London Kill Zone filtering
- Economic calendar news filter
- Market Structure Shift detection
- Fibonacci Action Zone retracement
- 1% risk management with 1:3 RR ratio
