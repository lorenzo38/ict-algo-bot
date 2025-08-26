#!/usr/bin/env python3
"""
ICT Algo Signal Bot - Render Deployment Version
Runs as scheduled job instead of continuous process.
"""

import threading
import time
from flask import Flask, jsonify
