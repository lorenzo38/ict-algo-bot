from datetime import datetime, time
import pytz

def is_london_kill_zone():
    """Check if current time is within London Kill Zone."""
    now_utc = datetime.now(pytz.UTC)
    current_time = now_utc.time()
    
    start_time = time(7, 0)
    end_time = time(11, 0)
    
    return start_time <= current_time <= end_time

def should_check_market():
    """
    Master function to determine if market conditions should be checked.
    Returns False outside kill zone or during news events.
    """
    from utils.news_filter import is_news_silence_period
    
    if not is_london_kill_zone():
        return False
        
    if not is_news_silence_period():
        return False
        
    return True
