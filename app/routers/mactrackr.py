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
            {"retailer": "amazon", "price": 799, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-128GB-White-Intelligence/dp/B0DHTYW7P8"},
            {"retailer": "bestbuy", "price": 799, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-16-128gb-white-verizon/JJGCQ866TH"},
            {"retailer": "walmart", "price": 799, "inStock": True, "url": "https://www.walmart.com/ip/iPhone-16-128GB-White-Apple-Intelligence/11469110090"},
            {"retailer": "target", "price": 799, "inStock": True, "url": "https://www.target.com/p/apple-iphone-16-128gb-white/-/A-86076262"},
            {"retailer": "bhphoto", "price": 799, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800534-REG/apple_myd53ll_a_iphone_16_128gb_white.html"},
            {"retailer": "adorama", "price": 799, "inStock": True, "url": "https://www.adorama.com/ac12816wh.html"}
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
            {"retailer": "amazon", "price": 1199, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-256GB-Desert-Titanium/dp/B0DHTZ4QQP"},
            {"retailer": "bestbuy", "price": 1199, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-16-pro-max-256gb-desert-titanium-verizon/JCQ6HRFWVW"},
            {"retailer": "walmart", "price": 1199, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPhone-16-Pro-Max-256GB-Desert-Titanium/5000354046"},
            {"retailer": "target", "price": 1199, "inStock": True, "url": "https://www.target.com/p/apple-iphone-16-pro-max/-/A-93597962"},
            {"retailer": "bhphoto", "price": 1199, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800550-REG/apple_mynn3ll_a_iphone_16_pro_max.html"},
            {"retailer": "adorama", "price": 1199, "inStock": True, "url": "https://www.adorama.com/ac25616pmaxdt.html"}
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
            {"retailer": "amazon", "price": 999, "inStock": True, "url": "https://www.amazon.com/Apple-MacBook-13-inch-10-Core-16-Core/dp/B0DKLHHMZ4"},
            {"retailer": "bestbuy", "price": 999, "inStock": True, "url": "https://www.bestbuy.com/site/apple-macbook-air-13-inch-laptop-apple-m4-chip-16gb-memory-256gb-ssd-midnight/6534616.p"},
            {"retailer": "walmart", "price": 999, "inStock": True, "url": "https://www.walmart.com/ip/Apple-13-inch-MacBook-Air-M4-w-10-core-CPU-and-8-core-GPU-256GB-SSD-Silver-MW0W3LL-A-2025/15481367422"},
            {"retailer": "bhphoto", "price": 999, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1811193-REG/apple_mw123ll_a_13_macbook_air_m4.html"},
            {"retailer": "adorama", "price": 999, "inStock": True, "url": "https://www.adorama.com/acmba1324sm4.html"}
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
            {"retailer": "amazon", "price": 1999, "inStock": True, "url": "https://www.amazon.com/Apple-MacBook-14-inch-14-Core-20-Core/dp/B0DKLHH7T4"},
            {"retailer": "bestbuy", "price": 1999, "inStock": True, "url": "https://www.bestbuy.com/site/apple-macbook-pro-14-inch-laptop-m4-pro-chip-24gb-memory-512gb-ssd-space-black/6534615.p"},
            {"retailer": "walmart", "price": 1999, "inStock": True, "url": "https://www.walmart.com/ip/Apple-14-MacBook-Pro-with-M4-Chip-10-Core-CPU-10-Core-GPU-24GB-Memory-1TB-SSD-Space-Black-2024/13679766551"},
            {"retailer": "bhphoto", "price": 1999, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1811194-REG/apple_mbp14m4_24gb_512.html"},
            {"retailer": "adorama", "price": 1999, "inStock": True, "url": "https://www.adorama.com/acmbp1424m4.html"}
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
            {"retailer": "amazon", "price": 599, "inStock": True, "url": "https://www.amazon.com/Apple-iPad-Air-11-inch-128GB/dp/B0D3J3C1QD"},
            {"retailer": "bestbuy", "price": 599, "inStock": True, "url": "https://www.bestbuy.com/site/apple-11-inch-ipad-air-m3-chip-wi-fi-128gb-space-gray/6534608.p"},
            {"retailer": "walmart", "price": 599, "inStock": True, "url": "https://www.walmart.com/ip/2025-Apple-11-inch-iPad-Air-M3-Built-for-Apple-Intelligence-Wi-Fi-128GB-Space-Gray/15450254481"},
            {"retailer": "target", "price": 599, "inStock": True, "url": "https://www.target.com/p/apple-ipad-air-m3-11-inch-wi-fi-128gb-space-gray/-/A-91122029"},
            {"retailer": "bhphoto", "price": 599, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1812268-REG/apple_ipad_air_11_m3_128gb.html"},
            {"retailer": "adorama", "price": 599, "inStock": True, "url": "https://www.adorama.com/acipadair11.html"}
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
            {"retailer": "amazon", "price": 599, "inStock": True, "url": "https://www.amazon.com/Apple-2024-Mac-Desktop-Computer/dp/B0DKLHHMZ5"},
            {"retailer": "bestbuy", "price": 599, "inStock": True, "url": "https://www.bestbuy.com/site/apple-mac-mini-desktop-m4-chip-16gb-memory-256gb-ssd-silver/6534617.p"},
            {"retailer": "walmart", "price": 599, "inStock": True, "url": "https://www.walmart.com/ip/Apple-2024-Mac-mini-Desktop-Computer-with-M4-chip-10-core-CPU-10-core-GPU-16GB-Unified-Memory-256GB/5406222929"},
            {"retailer": "bhphoto", "price": 599, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1811195-REG/apple_mac_mini_m4_256gb.html"},
            {"retailer": "adorama", "price": 599, "inStock": True, "url": "https://www.adorama.com/acmacminim4.html"}
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
            {"retailer": "amazon", "price": 399, "inStock": True, "url": "https://www.amazon.com/Apple-Watch-GPS-Aluminum-Sport/dp/B0DGHQ72MX"},
            {"retailer": "bestbuy", "price": 399, "inStock": True, "url": "https://www.bestbuy.com/site/apple-watch-series-10-gps-42mm-aluminum-case-with-black-sport-band-m-l-jet-black/6574960.p"},
            {"retailer": "walmart", "price": 399, "inStock": True, "url": "https://www.walmart.com/ip/Apple-Watch-Series-10-GPS-42mm-Jet-Black-Aluminum-Case-with-Black-Sport-Band-S-M/11385157008"},
            {"retailer": "target", "price": 399, "inStock": True, "url": "https://www.target.com/p/apple-watch-series-10-gps-42mm-jet-black-aluminum-case-with-black-sport-band-m-l/-/A-91122498"}
        ],
        "releaseDate": "2024-09-20"
    },
    {
        "id": "airpods-pro-2",
        "name": "AirPods Pro 2",
        "category": "airpods",
        "specs": {"chip": "H2", "features": "Active Noise Cancellation, Transparency, MagSafe Charging", "battery": "30h with case"},
        "prices": [
            {"retailer": "apple", "price": 249, "inStock": True, "url": "https://www.apple.com/shop/product/MTJV3AM/A/airpods-pro"},
            {"retailer": "amazon", "price": 229, "inStock": True, "url": "https://www.amazon.com/Apple-Generation-Cancelling-Transparency-Personalized/dp/B0D1XD1ZV3"},
            {"retailer": "bestbuy", "price": 249, "inStock": True, "url": "https://www.bestbuy.com/site/apple-airpods-pro-2-wireless-active-noise-cancelling-earbuds-hearing-aid-feature-bluetooth-headphones-with-magsafe-charging-case-usbc-white/5720312.p"},
            {"retailer": "walmart", "price": 229, "inStock": True, "url": "https://www.walmart.com/ip/Apple-AirPods-Pro-2-White/5043748016"},
            {"retailer": "target", "price": 249, "inStock": True, "url": "https://www.target.com/p/apple-airpods-pro-2nd-generation/-/A-85978618"},
            {"retailer": "bhphoto", "price": 249, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1733640-REG/apple_mtjv3am_a_airpods_pro_2nd.html"},
            {"retailer": "adorama", "price": 249, "inStock": True, "url": "https://www.adorama.com/acmtjv3ama.html"},
            {"retailer": "costco", "price": 239, "inStock": True, "url": "https://www.costco.com/apple-airpods-pro-2nd-generation.product.4000143838.html"}
        ],
        "releaseDate": "2023-09-22"
    },
    {
        "id": "airpods-4",
        "name": "AirPods 4",
        "category": "airpods",
        "specs": {"chip": "H2", "features": "Active Noise Cancellation, Spatial Audio, USB-C", "battery": "30h with case"},
        "prices": [
            {"retailer": "apple", "price": 179, "inStock": True, "url": "https://www.apple.com/shop/buy-airpods/airpods-4"},
            {"retailer": "amazon", "price": 169, "inStock": True, "url": "https://www.amazon.com/Apple-AirPods-4-Wireless-Earbuds/dp/B0D1XD5Z8Q"},
            {"retailer": "bestbuy", "price": 179, "inStock": True, "url": "https://www.bestbuy.com/site/apple-airpods-4-wireless-earbuds-active-noise-cancelling-bluetooth-headphones-with-magsafe-charging-case-usbc-white/6418599.p"},
            {"retailer": "walmart", "price": 169, "inStock": True, "url": "https://www.walmart.com/ip/Apple-AirPods-4-Active-Noise-Cancelling/11620163840"},
            {"retailer": "target", "price": 179, "inStock": True, "url": "https://www.target.com/p/apple-airpods-4-with-active-noise-cancellation/-/A-92635832"},
            {"retailer": "bhphoto", "price": 179, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1802197-REG/apple_airpods_4_with_active.html"},
            {"retailer": "adorama", "price": 179, "inStock": True, "url": "https://www.adorama.com/acairpods4anc.html"}
        ],
        "releaseDate": "2024-09-20"
    },
    {
        "id": "airpods-max",
        "name": "AirPods Max",
        "category": "airpods",
        "specs": {"chip": "H1", "features": "Active Noise Cancellation, Spatial Audio, Digital Crown", "battery": "20h"},
        "prices": [
            {"retailer": "apple", "price": 549, "inStock": True, "url": "https://www.apple.com/shop/buy-airpods/airpods-max"},
            {"retailer": "amazon", "price": 499, "inStock": True, "url": "https://www.amazon.com/Apple-AirPods-Max-Black-USB/dp/B0D1X6JJWQ"},
            {"retailer": "bestbuy", "price": 549, "inStock": True, "url": "https://www.bestbuy.com/site/apple-airpods-max-wireless-over-ear-headphones-active-noise-cancelling-bluetooth-space-gray/6418591.p"},
            {"retailer": "walmart", "price": 499, "inStock": True, "url": "https://www.walmart.com/ip/Apple-AirPods-Max-Space-Gray/15448637505"},
            {"retailer": "target", "price": 549, "inStock": True, "url": "https://www.target.com/p/apple-airpods-max/-/A-83651668"},
            {"retailer": "bhphoto", "price": 549, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1597291-REG/apple_airpods_max_silver.html"},
            {"retailer": "adorama", "price": 549, "inStock": True, "url": "https://www.adorama.com/acmmef2ama.html"}
        ],
        "releaseDate": "2024-12-11"
    },
    {
        "id": "airpods-4-standard",
        "name": "AirPods 4 (Standard)",
        "category": "airpods",
        "specs": {"chip": "H2", "features": "Spatial Audio, USB-C, No ANC", "battery": "30h with case"},
        "prices": [
            {"retailer": "apple", "price": 129, "inStock": True, "url": "https://www.apple.com/shop/buy-airpods/airpods-4"},
            {"retailer": "amazon", "price": 119, "inStock": True, "url": "https://www.amazon.com/Apple-AirPods-4-Wireless-Earbuds/dp/B0D1XD5Z8Q"},
            {"retailer": "bestbuy", "price": 129, "inStock": True, "url": "https://www.bestbuy.com/site/apple-airpods-4-wireless-earbuds-bluetooth-headphones-with-magsafe-charging-case-usbc-white/6418600.p"},
            {"retailer": "walmart", "price": 119, "inStock": True, "url": "https://www.walmart.com/ip/Apple-AirPods-4/5451953393"},
            {"retailer": "target", "price": 129, "inStock": True, "url": "https://www.target.com/p/apple-airpods-4/-/A-92635831"}
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