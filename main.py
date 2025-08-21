#!/usr/bin/env python3
"""
ICT Algo Signal Bot - Generates trading signals without MT5 dependency.
"""

import time
import schedule
from datetime import datetime
import pytz

from data.data_provider import fetch_market_data, get_current_price, initialize_mt5
from utils.time_utils import should_check_market
from core.market_structure import detect_mss
from core.fibonacci import calculate_action_zone
from core.entry_logic import check_entry_trigger
from signals.signal_manager import SignalManager
from outputs.console_output import print_signal

def run_bot_cycle():
    """Main bot execution cycle."""
    print(f"\n--- Bot Cycle: {datetime.now(pytz.UTC)} ---")
    
    # Check market conditions
    if not should_check_market():
        print("Outside trading hours or news silence breached. Skipping cycle.")
        return
    
    try:
        # Fetch market data from Yahoo Finance
        print("Fetching 4H data...")
        df_4h = fetch_market_data('XAU/GBP', 'H4', 100)
        print("Fetching 1H data...")
        df_1h = fetch_market_data('XAU/GBP', 'H1', 50)
        
        if df_4h is None or df_1h is None:
            print("Failed to fetch market data. Check internet connection.")
            return
        
        # Detect Market Structure Shift
        print("Analyzing market structure...")
        mss_info = detect_mss(df_4h)
        if not mss_info:
            print("No MSS detected.")
            return
        
        print(f"MSS detected: {mss_info['type'].upper()}")
        
        # Calculate Action Zone
        action_zone = calculate_action_zone(mss_info)
        print(f"Action Zone: {action_zone['low']:.2f} - {action_zone['high']:.2f}")
        
        # Check for entry trigger
        trigger = check_entry_trigger(df_1h, action_zone, mss_info['type'])
        if not trigger:
            print("No entry trigger detected.")
            return
        
        # Get current price for entry
        print("Getting current price...")
        current_price = get_current_price('XAU/GBP')
        if current_price is None:
            print("Failed to get current price.")
            return
        
        print(f"Current Price: {current_price}")
        
        # Generate and display signal
        signal_manager = SignalManager()
        signal = signal_manager.generate_signal(mss_info, action_zone, current_price, mss_info['type'])
        
        # Print to console and save to file
        print_signal(signal)
        filename = signal_manager.save_signal(signal)
        print(f"Signal saved to: {filename}")
        
    except Exception as e:
        print(f"Error in bot cycle: {e}")

def main():
    """Initialize and run the signal bot."""
    print("Starting ICT Algo Signal Bot - XAU/GBP")
    print("This bot generates trading signals without automatic execution.")
    print("You can manually enter trades based on these signals.")
    print("Press Ctrl+C to exit.\n")
    
    # Initialize (mock function for compatibility)
    initialize_mt5()
    
    try:
        # Schedule to run every hour
        schedule.every().hour.at(":01").do(run_bot_cycle)
        
        # Also run immediately
        run_bot_cycle()
        
        print("\nBot is running. Waiting for London trading hours...")
        print("Next check scheduled every hour.")
        
        while True:
            schedule.run_pending()
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nShutting down signal bot...")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
