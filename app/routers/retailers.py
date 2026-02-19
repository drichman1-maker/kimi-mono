"""
Retailer API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Retailer
from app.schemas import RetailerCreate, RetailerResponse

router = APIRouter(prefix="/retailers", tags=["retailers"])

@router.get("/", response_model=List[RetailerResponse])
def list_retailers(
    is_active: bool = True,
    scraper_type: str = None,
    db: Session = Depends(get_db)
):
    """List retailers"""
    query = db.query(Retailer)

    if is_active is not None:
        query = query.filter(Retailer.is_active == is_active)
    if scraper_type:
        query = query.filter(Retailer.scraper_type == scraper_type)

    return query.all()

@router.post("/", response_model=RetailerResponse)
def create_retailer(retailer: RetailerCreate, db: Session = Depends(get_db)):
    """Add a new retailer"""
    db_retailer = Retailer(**retailer.dict())
    db.add(db_retailer)
    db.commit()
    db.refresh(db_retailer)
    return db_retailer

@router.get("/{retailer_id}", response_model=RetailerResponse)
def get_retailer(retailer_id: int, db: Session = Depends(get_db)):
    """Get retailer details"""
    retailer = db.query(Retailer).filter(Retailer.id == retailer_id).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")
    return retailer

@router.put("/{retailer_id}")
def update_retailer(retailer_id: int, updates: RetailerCreate, db: Session = Depends(get_db)):
    """Update retailer"""
    retailer = db.query(Retailer).filter(Retailer.id == retailer_id).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")

    for field, value in updates.dict().items():
        setattr(retailer, field, value)

    db.commit()
    return retailer

@router.delete("/{retailer_id}")
def delete_retailer(retailer_id: int, db: Session = Depends(get_db)):
    """Delete retailer"""
    retailer = db.query(Retailer).filter(Retailer.id == retailer_id).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")

    db.delete(retailer)
    db.commit()
    return {"message": "Retailer deleted"}
