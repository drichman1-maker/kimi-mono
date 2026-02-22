"""
Telegram Notification Service
Sends price alerts to Telegram via bot API
"""

import os
import aiohttp
from typing import Optional
from datetime import datetime

# Get bot token from environment
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")  # Doug's chat ID

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


async def send_price_alert(
    product_name: str,
    current_price: float,
    previous_price: Optional[float],
    retailer_name: str,
    product_url: str,
    image_url: Optional[str] = None,
    target_price: Optional[float] = None
) -> bool:
    """
    Send a price drop alert to Telegram
    
    Args:
        product_name: Name of the product
        current_price: Current price
        previous_price: Previous price (for calculating drop %)
        retailer_name: Name of the retailer
        product_url: URL to the product
        image_url: Optional product image
        target_price: Optional target price that was set
    
    Returns:
        bool: True if message was sent successfully
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars.")
        return False
    
    # Calculate price drop
    price_drop = ""
    if previous_price and previous_price > current_price:
        drop_pct = ((previous_price - current_price) / previous_price) * 100
        price_drop = f"📉 Down {drop_pct:.1f}% from ${previous_price:.2f}\n"
    
    # Build message
    message = f"🚨 *Price Drop Alert*\n\n"
    message += f"*{product_name}*\n"
    message += f"💰 Current: *${current_price:.2f}*\n"
    message += price_drop
    if target_price:
        message += f"🎯 Target was: ${target_price:.2f}\n"
    message += f"🏪 {retailer_name}\n\n"
    message += f"[View Deal]({product_url})"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    print(f"✅ Telegram alert sent for {product_name}")
                    return True
                else:
                    error = await response.text()
                    print(f"❌ Telegram API error: {error}")
                    return False
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")
        return False


async def send_restocker_alert(
    product_name: str,
    retailer_name: str,
    product_url: str,
    price: Optional[float] = None,
    image_url: Optional[str] = None
) -> bool:
    """
    Send a restock alert (item back in stock)
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    
    message = f"📦 *Back in Stock*\n\n"
    message += f"*{product_name}*\n"
    if price:
        message += f"💰 ${price:.2f}\n"
    message += f"🏪 {retailer_name}\n\n"
    message += f"[Buy Now]({product_url})"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                return response.status == 200
    except Exception as e:
        print(f"❌ Failed to send restock alert: {e}")
        return False


async def send_daily_summary(products_tracked: int, alerts_sent: int, avg_price_changes: float) -> bool:
    """
    Send daily summary report
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    
    message = f"📊 *Daily Price Tracker Summary*\n\n"
    message += f"Products tracked: {products_tracked}\n"
    message += f"Alerts sent: {alerts_sent}\n"
    message += f"Avg price change: {avg_price_changes:.1f}%\n"
    message += f"\n_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                return response.status == 200
    except Exception as e:
        print(f"❌ Failed to send summary: {e}")
        return False
