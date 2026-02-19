"""
Pydantic Schemas for Request/Response Validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class Category(str, Enum):
    MAC = "mac"
    POKEMON = "pokemon"
    AUDIO = "audio"
    ELECTRONICS = "electronics"
    COLLECTIBLES = "collectibles"
    OTHER = "other"

class Condition(str, Enum):
    NEW = "new"
    USED = "used"
    REFURBISHED = "refurbished"
    OPEN_BOX = "open_box"

class PriceCondition(str, Enum):
    BELOW = "below"
    ABOVE = "above"

# Tier 1: Base Product Schema (Common fields)
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=500)
    category: Category
    description: Optional[str] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None

class ProductCreate(ProductBase):
    # Tier 2: Category-specific fields
    model_identifier: Optional[str] = None
    release_year: Optional[int] = None
    specs: Optional[Dict[str, Any]] = {}

    # Pokemon-specific
    set_name: Optional[str] = None
    card_number: Optional[str] = None
    rarity: Optional[str] = None
    condition: Optional[str] = None

    # Audio/Music
    brand: Optional[str] = None
    model: Optional[str] = None

    # Generic attributes
    attributes: Optional[Dict[str, Any]] = {}

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    is_active: Optional[bool] = None
    specs: Optional[Dict[str, Any]] = None
    attributes: Optional[Dict[str, Any]] = None

class ProductResponse(ProductBase):
    id: int
    model_identifier: Optional[str]
    release_year: Optional[int]
    specs: Dict[str, Any]
    set_name: Optional[str]
    card_number: Optional[str]
    rarity: Optional[str]
    condition: Optional[str]
    brand: Optional[str]
    model: Optional[str]
    attributes: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Price Schemas
class PriceBase(BaseModel):
    price: float = Field(..., gt=0)
    currency: str = "USD"
    condition: Optional[str] = None
    availability: Optional[str] = None

class PriceCreate(PriceBase):
    product_id: int
    retailer_id: int
    listing_url: Optional[str] = None
    listing_title: Optional[str] = None
    seller_rating: Optional[float] = None
    shipping_cost: Optional[float] = None

class PriceResponse(PriceBase):
    id: int
    product_id: int
    retailer_id: int
    listing_url: Optional[str]
    listing_title: Optional[str]
    seller_rating: Optional[float]
    shipping_cost: Optional[float]
    scraped_at: datetime

    class Config:
        from_attributes = True

class PriceWithRetailer(PriceResponse):
    retailer_name: str
    retailer_logo: Optional[str]

# Retailer Schemas
class RetailerBase(BaseModel):
    name: str
    base_url: str
    logo_url: Optional[str] = None
    scraper_type: str

class RetailerCreate(RetailerBase):
    config: Optional[Dict[str, Any]] = {}

class RetailerResponse(RetailerBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Alert Schemas
class PriceAlertBase(BaseModel):
    target_price: float = Field(..., gt=0)
    condition: PriceCondition = PriceCondition.BELOW
    email: Optional[str] = None
    webhook_url: Optional[str] = None

class PriceAlertCreate(PriceAlertBase):
    product_id: int

class PriceAlertResponse(PriceAlertBase):
    id: int
    product_id: int
    is_active: bool
    created_at: datetime
    last_triggered: Optional[datetime]
    trigger_count: int

    class Config:
        from_attributes = True

# Search & Filter Schemas
class ProductSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[Category] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    retailer_id: Optional[int] = None
    condition: Optional[str] = None

    # Tier 2 filters
    brand: Optional[str] = None
    model: Optional[str] = None
    release_year: Optional[int] = None
    set_name: Optional[str] = None
    rarity: Optional[str] = None

class ProductWithPrices(ProductResponse):
    prices: List[PriceWithRetailer]
    price_stats: Dict[str, Any]

class PriceComparison(BaseModel):
    product: ProductResponse
    prices: List[PriceWithRetailer]
    best_price: Optional[PriceWithRetailer]
    avg_price: float
    price_range: Dict[str, float]
