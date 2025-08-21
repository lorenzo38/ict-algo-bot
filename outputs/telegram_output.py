import requests
from config import settings

def send_telegram_message(message):
    """
    Send message to Telegram bot.
    """
    if not settings.TELEGRAM_ENABLED or not settings.TELEGRAM_BOT_TOKEN:
        print("Telegram notifications disabled or missing credentials")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
        
    except Exception as e:
        print(f"Telegram send error: {e}")
        return False

def send_telegram_signal(signal):
    """
    Format and send trading signal to Telegram.
    """
    from utils.time_utils import get_current_session
    
    session = get_current_session()
    session_emoji = "🇬🇧" if session == "london" else "🇺🇸"
    
    if signal['signal'] == 'BUY':
        emoji = '🟢'
        action = 'BUY'
    else:
        emoji = '🔴' 
        action = 'SELL'
    
    message = f"""
{emoji} <b>TRADING SIGNAL</b> {emoji} {session_emoji}

<b>Session:</b> {session.upper()}
<b>Action:</b> {action}
<b>Instrument:</b> {signal['instrument']}
<b>Entry:</b> {signal['entry_price']}
<b>Stop Loss:</b> {signal['stop_loss']}
<b>Take Profit:</b> {signal['take_profit']}
<b>Risk/Reward:</b> 1:{signal['risk_reward_ratio']}

<b>Time:</b> {signal['date_time_utc']}

✅ <b>Conditions Met:</b>
• MSS {signal['validation_data']['mss_type'].upper()} confirmed
• Price in Action Zone
• Strong close trigger

📊 <b>Action Zone:</b> {signal['validation_data']['action_zone_low']} - {signal['validation_data']['action_zone_high']}
    """
    
    return send_telegram_message(message)
