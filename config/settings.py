import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Trading Settings
SYMBOL = os.getenv('SYMBOL', 'XAU/GBP')
RISK_PERCENT = float(os.getenv('RISK_PERCENT', 1.0))
RR_RATIO = float(os.getenv('RR_RATIO', 3.0))
BUFFER_PIPS = 5.0

# Time Settings - Multiple Trading Sessions
LONDON_KILL_ZONE_START = "07:00"  # GMT
LONDON_KILL_ZONE_END = "11:00"    # GMT

NEWYORK_KILL_ZONE_START = "13:00"  # GMT (8:00 AM EST)
NEWYORK_KILL_ZONE_END = "17:00"    # GMT (12:00 PM EST)

NEWS_BUFFER_PRE = 15       # minutes before news
NEWS_BUFFER_POST = 90      # minutes after news
# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_ENABLED = os.getenv('TELEGRAM_ENABLED', 'true').lower() == 'true'
# Check if Telegram credentials are missing
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("⚠️  Telegram credentials not set. Notifications will be disabled.")
    TELEGRAM_ENABLED = False

# Economic Calendar API Settings (optional)
CALENDAR_API_URL = "https://api.calendar.trade/events"
RELEVANT_CURRENCIES = ["GBP", "USD", "CHF", "EUR", "XAU"]

# Logging Settings
LOG_LEVEL = "INFO"
