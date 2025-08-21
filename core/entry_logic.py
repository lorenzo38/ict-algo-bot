def check_entry_trigger(df_1h, action_zone, trend):
    """
    Check for entry trigger candle on 1H timeframe.
    
    Args:
        df_1h (pd.DataFrame): 1H OHLC data
        action_zone (dict): Action zone levels
        trend (str): 'bullish' or 'bearish'
        
    Returns:
        bool: True if entry trigger detected
    """
    current_candle = df_1h.iloc[-1]
    candle_range = current_candle['high'] - current_candle['low']
    
    if trend == 'bullish':
        # Check if candle closed above action zone in top 25% of range
        close_position = current_candle['close'] - current_candle['low']
        if (current_candle['close'] > action_zone['high'] and 
            (close_position / candle_range) >= 0.75):
            return True
    
    elif trend == 'bearish':
        # Check if candle closed below action zone in bottom 25% of range
        close_position = current_candle['high'] - current_candle['close']
        if (current_candle['close'] < action_zone['low'] and 
            (close_position / candle_range) >= 0.75):
            return True
    
    return False
