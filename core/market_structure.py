import pandas as pd
import numpy as np

def find_swing_points(high_series, low_series, lookback=3):
    """
    Identify swing highs and lows using a simple lookback method.
    
    Args:
        high_series (pd.Series): Series of high prices
        low_series (pd.Series): Series of low prices
        lookback (int): Number of bars to look back/forward
        
    Returns:
        tuple: (swing_highs, swing_lows) as DataFrames with datetime index and price
    """
    swing_highs = []
    swing_lows = []
    
    for i in range(lookback, len(high_series) - lookback):
        # Check for swing high
        if high_series.iloc[i] == high_series.iloc[i-lookback:i+lookback+1].max():
            swing_highs.append({
                'index': high_series.index[i],
                'price': high_series.iloc[i],
                'type': 'high'
            })
        
        # Check for swing low
        if low_series.iloc[i] == low_series.iloc[i-lookback:i+lookback+1].min():
            swing_lows.append({
                'index': low_series.index[i],
                'price': low_series.iloc[i],
                'type': 'low'
            })
    
    return pd.DataFrame(swing_highs), pd.DataFrame(swing_lows)

def detect_mss(df_4h, swing_lookback=5):
    """
    Detect Market Structure Shift on 4H timeframe.
    
    Returns:
        dict: MSS information or None if no MSS detected
    """
    swing_highs, swing_lows = find_swing_points(df_4h['high'], df_4h['low'], swing_lookback)
    
    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return None
    
    # Get latest swing points
    latest_swing_high = swing_highs.iloc[-1]['price']
    latest_swing_low = swing_lows.iloc[-1]['price']
    
    # Check for bullish MSS (break of swing high)
    current_close = df_4h['close'].iloc[-1]
    prev_close = df_4h['close'].iloc[-2]
    
    if current_close > latest_swing_high and current_close > prev_close:
        return {
            'type': 'bullish',
            'confirmation_candle': df_4h.iloc[-1],
            'swing_high': latest_swing_high,
            'swing_low': swing_lows.iloc[-2]['price'],  # Previous significant low
            'timestamp': df_4h.index[-1]
        }
    
    # Check for bearish MSS (break of swing low)
    if current_close < latest_swing_low and current_close < prev_close:
        return {
            'type': 'bearish',
            'confirmation_candle': df_4h.iloc[-1],
            'swing_low': latest_swing_low,
            'swing_high': swing_highs.iloc[-2]['price'],  # Previous significant high
            'timestamp': df_4h.index[-1]
        }
    
    return None
