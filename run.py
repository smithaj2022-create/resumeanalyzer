#!/usr/bin/env python3
"""
Production runner for Smart Resume Analyzer
Use this for deployment instead of app.py
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Production configuration
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 Starting Smart Resume Analyzer (Production Mode)")
    print(f"📍 Host: {host}")
    print(f"🔢 Port: {port}")
    print(f"🐛 Debug: {debug_mode}")
    print("=" * 50)
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode,
        threaded=True
    )