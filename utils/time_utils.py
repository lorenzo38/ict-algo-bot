from datetime import datetime, time
import pytz
from config import settings

def is_london_kill_zone():
    """Check if current time is within London Kill Zone."""
    now_utc = datetime.now(pytz.UTC)
    current_time = now_utc.time()
    
    start_time = time(7, 0)   # 07:00 GMT
    end_time = time(11, 0)    # 11:00 GMT
    
    return start_time <= current_time <= end_time

def is_newyork_kill_zone():
    """Check if current time is within New York Kill Zone."""
    now_utc = datetime.now(pytz.UTC)
    current_time = now_utc.time()
    
    start_time = time(13, 0)  # 13:00 GMT (8:00 AM EST)
    end_time = time(17, 0)    # 17:00 GMT (12:00 PM EST)
    
    return start_time <= current_time <= end_time

def is_any_trading_session():
    """Check if current time is within any trading session."""
    return is_london_kill_zone() or is_newyork_kill_zone()

def get_current_session():
    """Return the current active trading session."""
    if is_london_kill_zone():
        return "london"
    elif is_newyork_kill_zone():
        return "newyork"
    else:
        return None

def should_check_market():
    """
    Master function to determine if market conditions should be checked.
    Returns False outside trading sessions or during news events.
    """
    from utils.news_filter import is_news_silence_period
    
    if not is_any_trading_session():
        return False
        
    if not is_news_silence_period():
        return False
        
    return True