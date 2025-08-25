import yfinance as yf
import time
import pandas as pd


def get_close_price_safe(data, symbol):
    """
    Safely extract close price handling both old and new yfinance structures
    """
    if data is None or data.empty:
        return None
    
    try:
        # New multi-index structure (current yfinance)
        if isinstance(data.columns, pd.MultiIndex):
            return data['Close'][symbol].iloc[-1]
        else:
            # Old flat structure (legacy yfinance)
            return data['Close'].iloc[-1]
    except Exception as e:
        print(f"Error extracting close price for {symbol}: {e}")
        return None

def fetch_with_retry(symbol, period="1d", retries=3, delay=2):
    for attempt in range(retries):
        try:
            data = yf.download(symbol, period=period, timeout=30)
            if not data.empty:
                return data
        except Exception as e:
            print(f"Attempt {attempt + 1} for {symbol} failed: {e}")
            time.sleep(delay)
    return None

def get_xau_gbp():
    # Method 1: Try direct symbol
    direct_data = fetch_with_retry("XAUGBP=X", period="1d")
    if direct_data is not None and not direct_data.empty:
        return direct_data['Close'][symbol].iloc[-1]
    
    # Method 2: Calculate from USD rates (main fallback)
    gold_futures = fetch_with_retry("GC=F", period="1d")
    gbp_usd = fetch_with_retry("GBPUSD=X", period="1d")
    
    if gold_futures is not None and gbp_usd is not None:
        if not gold_futures.empty and not gbp_usd.empty:
            return gold_futures['Close']['GC=F'].iloc[-1] / gbp_usd['Close']['GBPUSD=X'].iloc[-1]
    
    # Method 3: Use gold futures as backup
    gold_futures = fetch_with_retry("GC=F", period="1d")
    if gold_futures is not None and gbp_usd is not None:
        if not gold_futures.empty and not gbp_usd.empty:
            return gold_futures['Close']['GC=F'].iloc[-1] / gbp_usd['Close']['GBPUSD=X'].iloc[-1]
    
    return None

# Test function
if __name__ == "__main__":
    price = get_xau_gbp()
    if price is not None:
        print(f"XAU/GBP price: {price}")
    else:
        print("Failed to retrieve XAU/GBP price")