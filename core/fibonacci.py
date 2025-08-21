def calculate_action_zone(mss_info):
    """
    Calculate Fibonacci retracement levels (50% to 78.6%) for the Action Zone.
    
    Args:
        mss_info (dict): MSS information from detect_mss()
        
    Returns:
        dict: Action zone high and low levels
    """
    if mss_info['type'] == 'bullish':
        impulse_low = mss_info['swing_low']
        impulse_high = mss_info['swing_high']
    else:  # bearish
        impulse_high = mss_info['swing_high']
        impulse_low = mss_info['swing_low']
    
    impulse_range = impulse_high - impulse_low
    
    # Calculate Fibonacci levels
    retrace_50 = impulse_high - (impulse_range * 0.50)
    retrace_786 = impulse_high - (impulse_range * 0.786)
    
    return {
        'high': retrace_50,
        'low': retrace_786,
        'impulse_high': impulse_high,
        'impulse_low': impulse_low
    }
