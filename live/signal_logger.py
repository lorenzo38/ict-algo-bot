import json
from datetime import datetime
from config import settings

def generate_signal_json(mss_info, action_zone, trigger, df_1h):
    """
    Generate the JSON signal object for logging.
    
    Args:
        mss_info (dict): MSS information
        action_zone (dict): Action zone levels
        trigger (bool): Entry trigger status
        df_1h (pd.DataFrame): 1H data for current prices
        
    Returns:
        dict: JSON signal object
    """
    current_price = df_1h['close'].iloc[-1]
    
    signal_data = {
        "signal": "BUY" if mss_info['type'] == 'bullish' else "SELL",
        "instrument": settings.SYMBOL,
        "logic_phase": 1,
        "date_time_utc": datetime.utcnow().isoformat(),
        "entry_price": current_price,
        "conditions_met": {
            "in_london_kill_zone": True,  # Assumed true since we're in kill zone
            "news_silence": True,         # Assumed true since we passed news check
            f"mss_{mss_info['type']}_confirmed": True,
            "price_in_action_zone_1h": True,
            f"{mss_info['type']}_close_trigger": trigger
        }
    }
    
    return signal_data
