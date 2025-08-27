#!/usr/bin/env python3
"""
ICT Algo Signal Bot - Render Deployment Version
Runs as scheduled job instead of continuous process.
"""

import sys
import os
from datetime import datetime
import pytz
import threading
import time
from flask import Flask, jsonify

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Health check endpoint for Render
app = Flask(__name__)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Bot is running"})

def run_health_server():
    app.run(host='0.0.0.0', port=5000)

# Start health server in background
health_thread = threading.Thread(target=run_health_server, daemon=True)
health_thread.start()

print("✅ Health server started on port 5000")

def run_single_cycle():
    """Run one complete analysis cycle."""
    print(f"🚀 Starting analysis cycle: {datetime.now(pytz.UTC)}")
    print(f"Symbol: XAU/GBP")
    print(f"Checking London Kill Zone: 07:00-11:00 GMT")

    try:
        # Import inside function to avoid circular imports
        from data.data_provider import fetch_market_data, get_current_price
        from utils.time_utils import should_check_market
        from core.market_structure import detect_mss
        from core.fibonacci import calculate_action_zone
        from core.entry_logic import check_entry_trigger
        from signals.signal_manager import SignalManager
        from outputs.console_output import print_signal

        # Check market conditions
        if not should_check_market():
            print("⏸️ Outside trading hours or news silence breached. Skipping cycle.")
            return {"status": "skipped", "reason": "outside_trading_hours"}

        # Fetch market data
        print("📊 Fetching market data...")
        df_4h = fetch_market_data('XAU/GBP', 'H4', 100)
        df_1h = fetch_market_data('XAU/GBP', 'H1', 50)

        if df_4h is None or df_1h is None:
            print("❌ Failed to fetch market data.")
            return {"status": "error", "reason": "data_fetch_failed"}

        # Detect Market Structure Shift
        print("🔍 Analyzing market structure...")
        mss_info = detect_mss(df_4h)
        if not mss_info:
            print("🔍 No MSS detected.")
            return {"status": "no_signal", "reason": "no_mss"}

        print(f"✅ MSS detected: {mss_info['type'].upper()}")

        # Calculate Action Zone
        action_zone = calculate_action_zone(mss_info)
        print(f"📈 Action Zone: {action_zone['low']:.2f} - {action_zone['high']:.2f}")

        # Check for entry trigger
        trigger = check_entry_trigger(df_1h, action_zone, mss_info['type'])
        if not trigger:
            print("🔍 No entry trigger detected.")
            return {"status": "no_signal", "reason": "no_trigger"}

        # Get current price for entry
        current_price = get_current_price('XAU/GBP')
        if current_price is None:
            print("❌ Failed to get current price.")
            return {"status": "error", "reason": "price_fetch_failed"}

        print(f"💰 Current Price: {current_price}")

        # Generate and display signal
        signal_manager = SignalManager()
        signal = signal_manager.generate_signal(mss_info, action_zone, current_price, mss_info['type'])

        # Print to console
        print_signal(signal)

        # Save to file
        filename = signal_manager.save_signal(signal)
        print(f"💾 Signal saved to: {filename}")

        # Send to Telegram
        telegram_sent = signal_manager.send_to_telegram(signal)

        return {
            "status": "signal_generated",
            "signal": signal,
            "telegram_sent": telegram_sent
        }

    except Exception as e:
        print(f"❌ Error in analysis cycle: {e}")
        return {"status": "error", "reason": str(e)}

if __name__ == "__main__":
    # This will run when executed directly (for testing)
    result = run_single_cycle()
    print(f"\n🎯 Cycle completed: {result['status']}")

    if result['status'] == 'signal_generated':
        print("✅ Trading signal generated and sent!")
    elif result['status'] == 'no_signal':
        print("ℹ️ No trading signal at this time.")
    else:
        print("❌ Analysis completed with errors.")
