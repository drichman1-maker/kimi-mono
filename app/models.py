"""
SQLAlchemy Models with Tier 1-2 Field Support
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Retailer(Base):
    __tablename__ = "retailers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    base_url = Column(String(500))
    logo_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    scraper_type = Column(String(50))  # 'ebay', 'pricecharting', 'reverb', 'custom'
    config = Column(JSON, default={})  # Scraper-specific config
    created_at = Column(DateTime, default=datetime.utcnow)

    prices = relationship("Price", back_populates="retailer")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # Tier 1: Common Fields (All categories)
    name = Column(String(500), index=True)
    category = Column(String(50), index=True)  # 'mac', 'pokemon', 'audio', etc.
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    source_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Tier 2: Category-Specific Fields (JSON for flexibility)
    # Mac Products
    model_identifier = Column(String(100), nullable=True)  # e.g., "Mac15,3"
    release_year = Column(Integer, nullable=True)
    specs = Column(JSON, default={})  # CPU, RAM, Storage, etc.

    # Pokemon Cards
    set_name = Column(String(100), nullable=True)
    card_number = Column(String(20), nullable=True)
    rarity = Column(String(50), nullable=True)
    condition = Column(String(20), nullable=True)  # 'NM', 'LP', 'MP', etc.

    # Audio/Music Gear
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)

    # Generic attributes storage
    attributes = Column(JSON, default={})  # Flexible storage for any category

    prices = relationship("Price", back_populates="product", cascade="all, delete-orphan")
    alerts = relationship("PriceAlert", back_populates="product", cascade="all, delete-orphan")

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    retailer_id = Column(Integer, ForeignKey("retailers.id"))

    price = Column(Float)
    currency = Column(String(3), default="USD")
    condition = Column(String(50), nullable=True)  # 'new', 'used', 'refurbished'
    availability = Column(String(50), nullable=True)  # 'in_stock', 'out_of_stock', 'preorder'

    # Additional metadata
    listing_url = Column(String(500), nullable=True)
    listing_title = Column(String(500), nullable=True)
    seller_rating = Column(Float, nullable=True)
    shipping_cost = Column(Float, nullable=True)

    scraped_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="prices")
    retailer = relationship("Retailer", back_populates="prices")

class PriceAlert(Base):
    __tablename__ = "price_alerts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))

    # Alert configuration
    target_price = Column(Float)
    condition = Column(String(20), default="below")  # 'below', 'above'
    is_active = Column(Boolean, default=True)

    # Notification settings
    email = Column(String(255), nullable=True)
    webhook_url = Column(String(500), nullable=True)

    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    last_triggered = Column(DateTime, nullable=True)
    trigger_count = Column(Integer, default=0)

    product = relationship("Product", back_populates="alerts")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    retailer_id = Column(Integer, ForeignKey("retailers.id"))

    price = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    # Market statistics
    avg_price = Column(Float, nullable=True)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
