import json
from datetime import datetime
import os
from config import settings
from outputs.telegram_output import send_telegram_signal

class SignalManager:
    def __init__(self):
        self.signals = []
        
    def generate_signal(self, mss_info, action_zone, current_price, trend):
        """
        Generate a complete trading signal.
        """
        # Calculate stop loss and take profit (5 pips buffer)
        pip_buffer = 0.05  # 5 pips for XAU/GBP (usually 2 decimal places)
        
        if trend == 'bullish':
            stop_loss = action_zone['impulse_low'] - pip_buffer
            take_profit = current_price + (3 * (current_price - stop_loss))
        else:
            stop_loss = action_zone['impulse_high'] + pip_buffer
            take_profit = current_price - (3 * (stop_loss - current_price))
        
        signal = {
            "signal": "BUY" if trend == 'bullish' else "SELL",
            "instrument": settings.SYMBOL,
            "date_time_utc": datetime.utcnow().isoformat(),
            "entry_price": round(current_price, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "risk_reward_ratio": 3.0,
            "conditions_met": {
                "in_london_kill_zone": True,
                "news_silence": True,
                f"mss_{trend}_confirmed": True,
                "price_in_action_zone": True,
                f"{trend}_close_trigger": True
            },
            "validation_data": {
                "mss_type": trend,
                "action_zone_high": round(action_zone['high'], 2),
                "action_zone_low": round(action_zone['low'], 2),
                "impulse_high": round(action_zone['impulse_high'], 2),
                "impulse_low": round(action_zone['impulse_low'], 2)
            }
        }
        
        self.signals.append(signal)
        return signal
    
    def save_signal(self, signal):
        """Save signal to JSON file."""
        # Ensure signals directory exists
        if not os.path.exists('signals'):
            os.makedirs('signals')
            
        filename = f"signals/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{signal['signal']}.json"
        with open(filename, 'w') as f:
            json.dump(signal, f, indent=2)
        return filename

    def send_to_telegram(self, signal):
        """Send signal to Telegram."""
        try:
            success = send_telegram_signal(signal)
            if success:
                print("✓ Signal sent to Telegram")
            else:
                print("✗ Failed to send to Telegram")
            return success
        except Exception as e:
            print(f"Telegram error: {e}")
            return False
