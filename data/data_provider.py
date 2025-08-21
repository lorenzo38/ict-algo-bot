import pandas as pd
import yfinance as yf
import requests
from config import settings

def fetch_market_data(symbol, timeframe, num_bars):
    """
    Fetch market data from Yahoo Finance (free, no API key needed).
    """
    # Map timeframe to Yahoo Finance interval
    interval_map = {
        'H1': '1h',
        'H4': '4h', 
        'D1': '1d'
    }
    
    # Convert symbol for Yahoo Finance
    yf_symbol = symbol.replace('/', '')
    if symbol == 'XAU/GBP':
        yf_symbol = 'XAUGBP=x'  # Yahoo Finance format for metals
    
    try:
        # Calculate period needed (enough days to get required bars)
        if timeframe == 'H1':
            period = f"{num_bars//24 + 2}d"  # 1H data: bars/24 hours per day + buffer
        elif timeframe == 'H4':
            period = f"{num_bars//6 + 2}d"   # 4H data: bars/6 per day + buffer
        else:
            period = f"{num_bars + 2}d"      # Daily data
    
        # Download data
        data = yf.download(
            tickers=yf_symbol,
            period=period,
            interval=interval_map.get(timeframe, '1h'),
            progress=False
        )
        
        if data.empty:
            print(f"No data returned for {yf_symbol}")
            return None
        
        # Rename columns to match MT5 format
        data = data.rename(columns={
            'Open': 'open',
            'High': 'high', 
            'Low': 'low',
            'Close': 'close',
            'Volume': 'tick_volume'
        })
        
        # Return the last num_bars
        return data.tail(num_bars)
        
    except Exception as e:
        print(f"Error fetching data from Yahoo Finance: {e}")
        return None

def get_current_price(symbol):
    """
    Get current price from Yahoo Finance.
    """
    try:
        yf_symbol = symbol.replace('/', '')
        if symbol == 'XAU/GBP':
            yf_symbol = 'XAUGBP=x'
            
        ticker = yf.Ticker(yf_symbol)
        data = ticker.history(period='1d', interval='1m')
        if data.empty:
            return None
        return round(data['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"Error getting current price: {e}")
        return None

# Mock functions for compatibility with existing code
def initialize_mt5():
    print("Running in signal-only mode. MT5 not required.")
    return True

def shutdown_mt5():
    print("Signal bot shutdown complete.")

def check_connection():
    return True
