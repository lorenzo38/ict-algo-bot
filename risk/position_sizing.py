import MetaTrader5 as mt5
from config import settings

def calculate_position_size(sl_price, entry_price, trend):
    """
    Calculate position size based on 1% account risk.
    
    Args:
        sl_price (float): Stop loss price
        entry_price (float): Entry price
        trend (str): 'bullish' or 'bearish'
        
    Returns:
        float: Position size in lots
    """
    # Calculate risk in pips
    if trend == 'bullish':
        risk_pips = (entry_price - sl_price) / 0.01  # Assuming 2 decimal places
    else:  # bearish
        risk_pips = (sl_price - entry_price) / 0.01
    
    # Get account equity
    account_info = mt5.account_info()
    if account_info is None:
        raise ValueError("Failed to get account info")
    
    equity = account_info.equity
    risk_amount = equity * (settings.RISK_PERCENT / 100)
    
    # Calculate position size (simplified - needs broker-specific pip value)
    position_size = risk_amount / (risk_pips * 1.0)  # Adjust for actual pip value
    
    return round(position_size, 2)
