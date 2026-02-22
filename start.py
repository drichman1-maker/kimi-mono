#!/usr/bin/env python3
"""
Production entry point - handles startup gracefully
v1.1 - Telegram alerts enabled
"""

import os
import uvicorn

def main():
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Price Aggregator API on {host}:{port}")
    print(f"📱 Telegram: {os.getenv('TELEGRAM_BOT_TOKEN', 'not configured')[:20]}...")
    print(f"🔌 DB: {os.getenv('DATABASE_URL', 'not set')[:30]}...")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        workers=1,
        log_level="info"
    )

if __name__ == "__main__":
    main()
