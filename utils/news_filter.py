import requests
from datetime import datetime, timedelta
from config import settings

def is_news_silence_period():
    """
    Check if current time is during news silence period.
    Returns True if no high-impact news, False during news events.
    """
    try:
        # This is a placeholder - implement actual API call
        # response = requests.get(f"{settings.CALENDAR_API_URL}?key={settings.CALENDAR_API_KEY}")
        # news_events = response.json()
        
        # For now, assume no news (always silent)
        return True
        
    except Exception as e:
        print(f"Error checking news: {e}")
        return False  # Be conservative - don't trade if news check fails
