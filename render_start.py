#!/usr/bin/env python3
"""
Render Start Script - Runs one analysis cycle and exits.
This is what Render will execute on each scheduled run.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from render_main import run_single_cycle

if __name__ == "__main__":
    print("🚀 Starting scheduled analysis cycle...")
    result = run_single_cycle()
    print(f"✅ Cycle completed with status: {result['status']}")
    sys.exit(0 if result['status'] != 'error' else 1)
