"""
Price Alert API Router
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import PriceAlert, Product, Price
from app.schemas import PriceAlertCreate, PriceAlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])

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
    """Manually trigger alert checking"""
    triggered = check_and_trigger_alerts(db)
    return {"checked": True, "triggered": triggered}

def check_and_trigger_alerts(db: Session):
    """Check all active alerts and trigger if conditions met"""
    alerts = db.query(PriceAlert).filter(PriceAlert.is_active == True).all()
    triggered = []

    for alert in alerts:
        latest_price = db.query(Price).filter(
            Price.product_id == alert.product_id
        ).order_by(Price.scraped_at.desc()).first()

        if not latest_price:
            continue

        condition_met = False
        if alert.condition == "below" and latest_price.price <= alert.target_price:
            condition_met = True
        elif alert.condition == "above" and latest_price.price >= alert.target_price:
            condition_met = True

        if condition_met:
            trigger_alert(alert, latest_price, db)
            triggered.append(alert.id)

    return triggered

def trigger_alert(alert, price, db):
    """Send alert notification"""
    alert.last_triggered = datetime.utcnow()
    alert.trigger_count += 1
    db.commit()

    # TODO: Implement email/webhook notification
    print(f"🚨 ALERT TRIGGERED: Product {alert.product_id} at ${price.price}")
