def print_signal(signal):
    """
    Print trading signal in readable format.
    """
    print("\n" + "="*60)
    print("🎯 TRADING SIGNAL GENERATED")
    print("="*60)
    print(f"Signal: {signal['signal']}")
    print(f"Instrument: {signal['instrument']}")
    print(f"Time: {signal['date_time_utc']}")
    print(f"Entry: {signal['entry_price']}")
    print(f"Stop Loss: {signal['stop_loss']}")
    print(f"Take Profit: {signal['take_profit']}")
    print(f"Risk/Reward: 1:{signal['risk_reward_ratio']}")
    print("\n📊 Conditions Met:")
    for condition, met in signal['conditions_met'].items():
        print(f"  • {condition}: {'✅' if met else '❌'}")
    print("="*60)
    
    # Also show validation data
    print("\n📈 Validation Data:")
    for key, value in signal['validation_data'].items():
        print(f"  • {key}: {value}")
    print("="*60)
