"""
Product API Router with Tier 1-2 Field Support
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Product, Price, Retailer
from app.schemas import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductSearch, ProductWithPrices, PriceComparison,
    PriceCreate, PriceResponse, Category
)

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[Category] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List products with optional filtering"""
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category.value)

    if search:
        search_filter = or_(
            Product.name.ilike(f"%{search}%"),
            Product.description.ilike(f"%{search}%"),
            Product.brand.ilike(f"%{search}%"),
            Product.model.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    return query.offset(skip).limit(limit).all()

@router.post("/search", response_model=List[ProductWithPrices])
def search_products(
    filters: ProductSearch,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Advanced search with Tier 1-2 filters"""
    query = db.query(Product).outerjoin(Price)

    # Tier 1: Common filters
    if filters.query:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{filters.query}%"),
                Product.description.ilike(f"%{filters.query}%")
            )
        )

    if filters.category:
        query = query.filter(Product.category == filters.category.value)

    # Price range filter
    if filters.min_price is not None:
        query = query.filter(Price.price >= filters.min_price)
    if filters.max_price is not None:
        query = query.filter(Price.price <= filters.max_price)

    # Tier 2: Category-specific vertical filters
    if filters.brand:
        query = query.filter(Product.brand.ilike(f"%{filters.brand}%"))

    if filters.model:
        query = query.filter(Product.model.ilike(f"%{filters.model}%"))

    if filters.release_year:
        query = query.filter(Product.release_year == filters.release_year)

    if filters.set_name:
        query = query.filter(Product.set_name.ilike(f"%{filters.set_name}%"))

    if filters.rarity:
        query = query.filter(Product.rarity.ilike(f"%{filters.rarity}%"))

    if filters.condition:
        query = query.filter(Product.condition == filters.condition)

    products = query.offset(skip).limit(limit).all()

    # Enrich with price data
    result = []
    for product in products:
        prices = db.query(Price).filter(Price.product_id == product.id).all()
        price_list = []
        for p in prices:
            retailer = db.query(Retailer).filter(Retailer.id == p.retailer_id).first()
            price_list.append({
                **p.__dict__,
                "retailer_name": retailer.name if retailer else "Unknown",
                "retailer_logo": retailer.logo_url if retailer else None
            })

        # Calculate stats
        if price_list:
            prices_only = [p.price for p in prices]
            stats = {
                "count": len(prices),
                "avg": round(sum(prices_only) / len(prices_only), 2),
                "min": min(prices_only),
                "max": max(prices_only)
            }
        else:
            stats = {"count": 0, "avg": 0, "min": 0, "max": 0}

        result.append({
            **product.__dict__,
            "prices": price_list,
            "price_stats": stats
        })

    return result

@router.get("/categories")
def get_categories():
    """Get available product categories"""
    return [
        {"id": "mac", "name": "Apple/Mac Products", "tier2_fields": ["model_identifier", "release_year", "specs"]},
        {"id": "pokemon", "name": "Pokemon Cards", "tier2_fields": ["set_name", "card_number", "rarity", "condition"]},
        {"id": "audio", "name": "Audio/Music Gear", "tier2_fields": ["brand", "model"]},
        {"id": "electronics", "name": "Electronics", "tier2_fields": ["brand", "model", "specs"]},
        {"id": "collectibles", "name": "Collectibles", "tier2_fields": ["condition", "rarity"]},
        {"id": "other", "name": "Other", "tier2_fields": []}
    ]

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product with Tier 1-2 fields"""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=ProductWithPrices)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product details with all prices"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    prices = db.query(Price).filter(Price.product_id == product_id).all()
    price_list = []
    for p in prices:
        retailer = db.query(Retailer).filter(Retailer.id == p.retailer_id).first()
        price_list.append({
            **p.__dict__,
            "retailer_name": retailer.name if retailer else "Unknown",
            "retailer_logo": retailer.logo_url if retailer else None
        })

    if price_list:
        prices_only = [p.price for p in prices]
        stats = {
            "count": len(prices),
            "avg": round(sum(prices_only) / len(prices_only), 2),
            "min": min(prices_only),
            "max": max(prices_only)
        }
    else:
        stats = {"count": 0, "avg": 0, "min": 0, "max": 0}

    return {
        **product.__dict__,
        "prices": price_list,
        "price_stats": stats
    }

@router.get("/{product_id}/comparison", response_model=PriceComparison)
def compare_prices(product_id: int, db: Session = Depends(get_db)):
    """Compare prices across retailers"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    prices = db.query(Price).filter(Price.product_id == product_id).order_by(Price.price).all()

    price_list = []
    for p in prices:
        retailer = db.query(Retailer).filter(Retailer.id == p.retailer_id).first()
        price_list.append({
            **p.__dict__,
            "retailer_name": retailer.name if retailer else "Unknown",
            "retailer_logo": retailer.logo_url if retailer else None
        })

    prices_only = [p.price for p in prices] if prices else [0]

    return {
        "product": product,
        "prices": price_list,
        "best_price": price_list[0] if price_list else None,
        "avg_price": round(sum(prices_only) / len(prices_only), 2),
        "price_range": {
            "min": min(prices_only),
            "max": max(prices_only)
        }
    }

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """Update product details"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# Price endpoints
@router.post("/{product_id}/prices", response_model=PriceResponse)
def add_price(product_id: int, price: PriceCreate, db: Session = Depends(get_db)):
    """Add a price entry for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_price = Price(**price.dict(), product_id=product_id)
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

@router.get("/{product_id}/prices/history")
def get_price_history(
    product_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get price history for a product"""
    from datetime import timedelta

    cutoff = datetime.utcnow() - timedelta(days=days)

    history = db.query(Price).filter(
        Price.product_id == product_id,
        Price.scraped_at >= cutoff
    ).order_by(Price.scraped_at).all()

    return {
        "product_id": product_id,
        "days": days,
        "data_points": len(history),
        "history": [
            {
                "price": h.price,
                "retailer_id": h.retailer_id,
                "scraped_at": h.scraped_at
            }
            for h in history
        ]
    }
