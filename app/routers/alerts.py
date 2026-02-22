"""
Price Alert API Router with Telegram Notifications
"""

import os
import asyncio
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models import PriceAlert, Product, Price, Retailer
from app.schemas import PriceAlertCreate, PriceAlertResponse
from app.services.telegram_service import send_price_alert, send_restocker_alert, send_daily_summary

router = APIRouter(prefix="/alerts", tags=["alerts"])

# Cron secret for webhook authentication
CRON_SECRET = os.getenv("CRON_SECRET", "your-secret-key-change-in-production")

@router.get("/", response_model=List[PriceAlertResponse])
def list_alerts(
    product_id: Optional[int] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """List price alerts"""
    query = db.query(PriceAlert)

    if product_id:
        query = query.filter(PriceAlert.product_id == product_id)
    if is_active is not None:
        query = query.filter(PriceAlert.is_active == is_active)

    return query.all()

@router.post("/", response_model=PriceAlertResponse)
def create_alert(alert: PriceAlertCreate, db: Session = Depends(get_db)):
    """Create a new price alert"""
    product = db.query(Product).filter(Product.id == alert.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_alert = PriceAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/{alert_id}", response_model=PriceAlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get alert details"""
    alert = db.query(PriceAlert).filter(PriceAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.put("/{alert_id}/toggle")
def toggle_alert(alert_id: int, db: Session = Depends(get_db)):
    """Toggle alert active status"""
    alert = db.query(PriceAlert).filter(PriceAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_active = not alert.is_active
    db.commit()
    return {"id": alert_id, "is_active": alert.is_active}

@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """Delete an alert"""
    alert = db.query(PriceAlert).filter(PriceAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()
    return {"message": "Alert deleted"}

@router.post("/check")
def check_alerts(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Manually trigger alert checking (admin use)"""
    triggered = check_and_trigger_alerts(db)
    return {"checked": True, "triggered": triggered}


@router.post("/trigger-check")
async def trigger_check_webhook(
    background_tasks: BackgroundTasks,
    x_cron_secret: Optional[str] = Header(None),
    check_type: str = "price_drops",  # price_drops, restocks, summary
    db: Session = Depends(get_db)
):
    """
    Webhook endpoint for cron jobs (GitHub Actions, cron-job.org, etc.)
    
    Headers:
        X-Cron-Secret: Secret key for authentication
    
    Query params:
        check_type: Type of check to run (price_drops, restocks, summary)
    """
    # Verify secret (optional but recommended)
    if CRON_SECRET != "your-secret-key-change-in-production":
        if x_cron_secret != CRON_SECRET:
            raise HTTPException(status_code=401, detail="Invalid cron secret")
    
    results = {"type": check_type, "timestamp": datetime.utcnow().isoformat()}
    
    if check_type == "price_drops":
        triggered = await check_and_trigger_alerts_async(db)
        results["alerts_triggered"] = len(triggered)
        results["alert_ids"] = triggered
    
    elif check_type == "restocks":
        restocked = await check_restock_alerts(db)
        results["restocked_items"] = len(restocked)
        results["items"] = restocked
    
    elif check_type == "summary":
        summary = await generate_daily_summary(db)
        results["summary"] = summary
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown check_type: {check_type}")
    
    return results


async def check_and_trigger_alerts_async(db: Session):
    """Async version of alert checking with Telegram notifications"""
    alerts = db.query(PriceAlert).filter(PriceAlert.is_active == True).all()
    triggered = []

    for alert in alerts:
        # Get latest price
        latest_price = db.query(Price).filter(
            Price.product_id == alert.product_id
        ).order_by(Price.scraped_at.desc()).first()

        if not latest_price:
            continue

        # Get previous price (2nd most recent) for drop detection
        previous_price = db.query(Price).filter(
            Price.product_id == alert.product_id,
            Price.id != latest_price.id
        ).order_by(Price.scraped_at.desc()).first()

        condition_met = False
        
        # Check target price condition
        if alert.condition == "below" and latest_price.price <= alert.target_price:
            condition_met = True
        elif alert.condition == "above" and latest_price.price >= alert.target_price:
            condition_met = True
        
        # Also trigger on significant price drops (>5%) even without target
        if not condition_met and previous_price:
            price_drop_pct = ((previous_price.price - latest_price.price) / previous_price.price) * 100
            if price_drop_pct >= 5:  # 5% or more drop
                condition_met = True
        
        # Don't re-trigger within 24 hours
        if alert.last_triggered and (datetime.utcnow() - alert.last_triggered) < timedelta(hours=24):
            condition_met = False

        if condition_met:
            await trigger_alert_async(alert, latest_price, previous_price, db)
            triggered.append(alert.id)

    return triggered


def check_and_trigger_alerts(db: Session):
    """Synchronous wrapper for compatibility"""
    return asyncio.run(check_and_trigger_alerts_async(db))


async def trigger_alert_async(alert, price, previous_price, db):
    """Send alert notification via Telegram"""
    alert.last_triggered = datetime.utcnow()
    alert.trigger_count += 1
    db.commit()

    # Get product and retailer details
    product = db.query(Product).filter(Product.id == alert.product_id).first()
    retailer = db.query(Retailer).filter(Retailer.id == price.retailer_id).first()
    
    if not product:
        print(f"⚠️ Product {alert.product_id} not found for alert")
        return

    # Send Telegram notification
    await send_price_alert(
        product_name=product.name,
        current_price=price.price,
        previous_price=previous_price.price if previous_price else None,
        retailer_name=retailer.name if retailer else "Unknown",
        product_url=price.listing_url or product.source_url or "",
        image_url=product.image_url,
        target_price=alert.target_price
    )
    
    print(f"🚨 ALERT SENT: {product.name} at ${price.price}")


async def check_restock_alerts(db: Session):
    """Check for items that came back in stock"""
    # Find products that were out of stock but now have prices
    # This is simplified - you'd want more sophisticated logic
    
    restocked = []
    
    # Get products with recent price updates that had no prices before
    recent_prices = db.query(Price).filter(
        Price.scraped_at >= datetime.utcnow() - timedelta(hours=1)
    ).all()
    
    for price in recent_prices:
        # Check if this product had no prices in the last 24h (was out of stock)
        old_price = db.query(Price).filter(
            Price.product_id == price.product_id,
            Price.scraped_at < datetime.utcnow() - timedelta(hours=24)
        ).order_by(Price.scraped_at.desc()).first()
        
        if not old_price:  # Was out of stock, now has price
            product = db.query(Product).filter(Product.id == price.product_id).first()
            retailer = db.query(Retailer).filter(Retailer.id == price.retailer_id).first()
            
            if product:
                await send_restocker_alert(
                    product_name=product.name,
                    retailer_name=retailer.name if retailer else "Unknown",
                    product_url=price.listing_url or product.source_url or "",
                    price=price.price,
                    image_url=product.image_url
                )
                restocked.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": price.price
                })
    
    return restocked


async def generate_daily_summary(db: Session):
    """Generate and send daily summary"""
    # Count tracked products
    products_count = db.query(Product).filter(Product.is_active == True).count()
    
    # Count prices updated in last 24h
    recent_updates = db.query(Price).filter(
        Price.scraped_at >= datetime.utcnow() - timedelta(hours=24)
    ).count()
    
    # Calculate average price change
    # (Simplified - you'd want proper calculation)
    avg_change = 0.0
    
    await send_daily_summary(
        products_tracked=products_count,
        alerts_sent=recent_updates,
        avg_price_changes=avg_change
    )
    
    return {
        "products_tracked": products_count,
        "recent_updates": recent_updates,
        "avg_price_change": avg_change
    }
