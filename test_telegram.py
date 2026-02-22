"""
Test script for Telegram price alerts
Usage: python test_telegram.py
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.services.telegram_service import send_price_alert, send_restocker_alert, send_daily_summary


async def test_alerts():
    """Test all Telegram alert types"""
    
    print("🧪 Testing Telegram alerts...")
    print(f"Bot token configured: {'Yes' if os.getenv('TELEGRAM_BOT_TOKEN') else 'No'}")
    print(f"Chat ID configured: {'Yes' if os.getenv('TELEGRAM_CHAT_ID') else 'No'}")
    
    # Test 1: Price drop alert
    print("\n📤 Sending price drop alert...")
    result1 = await send_price_alert(
        product_name="MacBook Air M3 15-inch (2024)",
        current_price=1099.00,
        previous_price=1299.00,
        retailer_name="Amazon",
        product_url="https://amazon.com/dp/B0CX23V2ZK",
        target_price=1100.00
    )
    print(f"✅ Price alert sent: {result1}")
    
    # Wait a bit between messages
    await asyncio.sleep(2)
    
    # Test 2: Restock alert
    print("\n📤 Sending restock alert...")
    result2 = await send_restocker_alert(
        product_name="NVIDIA RTX 4090 Founders Edition",
        retailer_name="Best Buy",
        product_url="https://bestbuy.com/rtx4090",
        price=1599.99
    )
    print(f"✅ Restock alert sent: {result2}")
    
    await asyncio.sleep(2)
    
    # Test 3: Daily summary
    print("\n📤 Sending daily summary...")
    result3 = await send_daily_summary(
        products_tracked=156,
        alerts_sent=12,
        avg_price_changes=-3.5
    )
    print(f"✅ Summary sent: {result3}")
    
    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    asyncio.run(test_alerts())
