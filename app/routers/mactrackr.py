"""
MacTrackr Compatibility Router
Serves static product data with direct retailer URLs
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api", tags=["mactrackr"])

# Product models
class PricePoint(BaseModel):
    retailer: str
    price: int
    inStock: bool
    url: str

class Product(BaseModel):
    id: str
    name: str
    category: str
    specs: dict
    prices: List[PricePoint]
    releaseDate: Optional[str] = None

# Static product data with direct URLs
PRODUCTS = [
    {
        "id": "iphone-16-128-unlocked",
        "name": "iPhone 16",
        "category": "iphone",
        "specs": {"storage": "128GB", "color": "White", "display": "6.1\" Super Retina XDR", "camera": "48MP Fusion"},
        "prices": [
            {"retailer": "apple", "price": 799, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-16"},
            {"retailer": "bestbuy", "price": 799, "inStock": True, "url": "https://www.bestbuy.com/site/product/apple-iphone-16-128gb-unlocked-white/JJGCQ866TH"},
            {"retailer": "walmart", "price": 799, "inStock": True, "url": "https://www.walmart.com/ip/iPhone-16-128GB-White-Apple-Intelligence/11469110090"},
            {"retailer": "target", "price": 799, "inStock": True, "url": "https://www.target.com/p/apple-iphone-16-128gb-white/-/A-86076262"}
        ],
        "releaseDate": "2024-09-20"
    },
    {
        "id": "iphone-16-pro-max-256",
        "name": "iPhone 16 Pro Max",
        "category": "iphone",
        "specs": {"storage": "256GB", "color": "Desert Titanium", "display": "6.9\" Super Retina XDR", "camera": "48MP Fusion"},
        "prices": [
            {"retailer": "apple", "price": 1199, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-16-pro-max"},
            {"retailer": "bestbuy", "price": 1199, "inStock": True, "url": "https://www.bestbuy.com/product/apple-iphone-16-pro-max-256gb-apple-intelligence-desert-titanium-verizon/JCQ6HRFWVW"},
            {"retailer": "walmart", "price": 1199, "inStock": True, "url": "https://www.walmart.com/ip/Restored-Apple-iPhone-16-Pro-Max-Carrier-Unlocked-256GB-Desert-Titanium-Refurbished/13333953014"},
            {"retailer": "target", "price": 1199, "inStock": True, "url": "https://www.target.com/p/apple-iphone-16-pro-max/-/A-93597962"}
        ],
        "releaseDate": "2024-09-20"
    },
    {
        "id": "macbook-air-13-m4",
        "name": "MacBook Air 13\"",
        "category": "mac",
        "specs": {"chip": "M4", "ram": "16GB", "storage": "256GB SSD", "display": "13.6\" Liquid Retina"},
        "prices": [
            {"retailer": "apple", "price": 999, "inStock": True, "url": "https://www.apple.com/shop/buy-mac/macbook-air/13-inch"},
            {"retailer": "bestbuy", "price": 999, "inStock": True, "url": "https://www.bestbuy.com/product/apple-macbook-air-13-inch-laptop-apple-m4-chip-built-for-apple-intelligence-16gb-memory-256gb-ssd-midnight/JJGCQ8RH7G"},
            {"retailer": "walmart", "price": 999, "inStock": True, "url": "https://www.walmart.com/ip/Apple-13-inch-MacBook-Air-M4-w-10-core-CPU-and-8-core-GPU-256GB-SSD-Silver-MW0W3LL-A-2025/15481367422"}
        ],
        "releaseDate": "2025-03-01"
    },
    {
        "id": "macbook-pro-14-m4",
        "name": "MacBook Pro 14\"",
        "category": "mac",
        "specs": {"chip": "M4", "ram": "24GB", "storage": "512GB SSD", "display": "14.2\" XDR"},
        "prices": [
            {"retailer": "apple", "price": 1999, "inStock": True, "url": "https://www.apple.com/shop/buy-mac/macbook-pro/14-inch"},
            {"retailer": "bestbuy", "price": 1999, "inStock": True, "url": "https://www.bestbuy.com/product/apple-macbook-pro-14-inch-laptop-apple-m4-pro-chip-built-for-apple-intelligence-24gb-memory-512gb-ssd-space-black/JJGCQ8HVWL"},
            {"retailer": "walmart", "price": 1999, "inStock": True, "url": "https://www.walmart.com/ip/Apple-14-MacBook-Pro-with-M4-Chip-10-Core-CPU-10-Core-GPU-24GB-Memory-1TB-SSD-Space-Black-2024/13679766551"}
        ],
        "releaseDate": "2024-11-01"
    },
    {
        "id": "ipad-air-11-m3",
        "name": "iPad Air 11\"",
        "category": "ipad",
        "specs": {"chip": "M3", "storage": "128GB", "display": "11\" Liquid Retina"},
        "prices": [
            {"retailer": "apple", "price": 599, "inStock": True, "url": "https://www.apple.com/shop/buy-ipad/ipad-air/11-inch-display-128gb-space-gray-wifi"},
            {"retailer": "bestbuy", "price": 599, "inStock": True, "url": "https://www.bestbuy.com/product/apple-11-inch-ipad-air-m3-chip-built-for-apple-intelligence-wi-fi-128gb-space-gray/JJGCQ8VZQH"},
            {"retailer": "walmart", "price": 599, "inStock": True, "url": "https://www.walmart.com/ip/2025-Apple-11-inch-iPad-Air-M3-Built-for-Apple-Intelligence-Wi-Fi-128GB-Space-Gray/15450254481"},
            {"retailer": "target", "price": 599, "inStock": True, "url": "https://www.target.com/p/apple-ipad-air-m3-11-inch-wi-fi-128gb-space-gray/-/A-91122029"}
        ],
        "releaseDate": "2025-03-01"
    },
    {
        "id": "mac-mini-m4",
        "name": "Mac mini",
        "category": "mac",
        "specs": {"chip": "M4", "ram": "16GB", "storage": "256GB SSD"},
        "prices": [
            {"retailer": "apple", "price": 599, "inStock": True, "url": "https://www.apple.com/shop/buy-mac/mac-mini/m4"},
            {"retailer": "bestbuy", "price": 599, "inStock": True, "url": "https://www.bestbuy.com/product/apple-mac-mini-desktop-latest-model-m4-chip-built-for-apple-intelligence-16gb-memory-256gb-ssd-silver/JJGCQXH2S4"}
        ],
        "releaseDate": "2025-03-01"
    },
    {
        "id": "apple-watch-series-10",
        "name": "Apple Watch Series 10",
        "category": "watch",
        "specs": {"size": "42mm", "case": "Jet Black Aluminum", "band": "Black Sport Band"},
        "prices": [
            {"retailer": "apple", "price": 399, "inStock": True, "url": "https://www.apple.com/shop/buy-watch/apple-watch"},
            {"retailer": "bestbuy", "price": 399, "inStock": True, "url": "https://www.bestbuy.com/product/apple-watch-series-10-gps-42mm-aluminum-case-with-black-sport-band-m-l-jet-black-2024/JJGCQ345P3"},
            {"retailer": "walmart", "price": 399, "inStock": True, "url": "https://www.walmart.com/ip/Apple-Watch-Series-10-GPS-42mm-Jet-Black-Aluminum-Case-with-Black-Sport-Band-S-M/11385157008"},
            {"retailer": "target", "price": 399, "inStock": True, "url": "https://www.target.com/p/apple-watch-series-10-gps-42mm-jet-black-aluminum-case-with-black-sport-band-m-l/-/A-91122498"}
        ],
        "releaseDate": "2024-09-20"
    }
]

@router.get("/products", response_model=List[dict])
def get_products(category: str = None):
    """Get products, optionally filtered by category"""
    if category:
        return [p for p in PRODUCTS if p["category"] == category]
    return PRODUCTS

@router.get("/products/{id}", response_model=dict)
def get_product(id: str):
    """Get single product by ID"""
    for p in PRODUCTS:
        if p["id"] == id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/categories")
def get_categories():
    """Get all categories with counts"""
    cats = {}
    for p in PRODUCTS:
        cats[p["category"]] = cats.get(p["category"], 0) + 1
    return [{"id": k, "label": k.capitalize(), "count": v} for k, v in cats.items()]