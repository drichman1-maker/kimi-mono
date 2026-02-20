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
            {"retailer": "adorama", "price": 799, "inStock": True, "url": "https://www.adorama.com/ac12816wh.html"},
            {"retailer": "ebay", "price": 749, "inStock": True, "url": "https://www.ebay.com/sch/i.html?_nkw=iPhone+16+128GB"}
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
            {"retailer": "adorama", "price": 1199, "inStock": True, "url": "https://www.adorama.com/ac25616pmaxdt.html"},
            {"retailer": "ebay", "price": 1149, "inStock": True, "url": "https://www.ebay.com/sch/i.html?_nkw=iPhone+16+Pro+Max+256GB"}
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
            {"retailer": "adorama", "price": 999, "inStock": True, "url": "https://www.adorama.com/acmba1324sm4.html"},
            {"retailer": "ebay", "price": 949, "inStock": True, "url": "https://www.ebay.com/sch/i.html?_nkw=MacBook+Air+13+M4"}
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
            {"retailer": "costco", "price": 239, "inStock": True, "url": "https://www.costco.com/apple-airpods-pro-2nd-generation.product.4000143838.html"},
            {"retailer": "ebay", "price": 219, "inStock": True, "url": "https://www.ebay.com/sch/i.html?_nkw=AirPods+Pro+2+USB-C"}
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
    },
    // === NEW PRODUCTS FROM PDF (M4 Generation + iPhone 16 Series) ===
    // iPhone 16 Pro Max variants
    {
        "id": "iphone-16-pro-max-512",
        "name": "iPhone 16 Pro Max",
        "category": "iphone",
        "specs": {"storage": "512GB", "color": "Natural Titanium", "display": "6.9\" Super Retina XDR", "camera": "48MP Fusion"},
        "prices": [
            {"retailer": "apple", "price": 1399, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-16-pro-max"},
            {"retailer": "amazon", "price": 1399, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-512GB-Natural-Titanium/dp/B0DHTZCKW7"},
            {"retailer": "bestbuy", "price": 1399, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-16-pro-max-512gb-natural-titanium/MYWE3LL-A"},
            {"retailer": "walmart", "price": 1399, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPhone-16-Pro-Max-512GB-Natural-Titanium/5000354047"},
            {"retailer": "bhphoto", "price": 1399, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800551-REG/apple_mywe3ll_a_iphone_16_pro_max_512gb.html"},
            {"retailer": "adorama", "price": 1399, "inStock": True, "url": "https://www.adorama.com/ac51216pmaxnt.html"}
        ],
        "releaseDate": "2024-09-20"
    },
    {
        "id": "iphone-16-pro-max-1tb",
        "name": "iPhone 16 Pro Max",
        "category": "iphone",
        "specs": {"storage": "1TB", "color": "Natural Titanium", "display": "6.9\" Super Retina XDR", "camera": "48MP Fusion"},
        "prices": [
            {"retailer": "apple", "price": 1599, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-16-pro-max"},
            {"retailer": "amazon", "price": 1599, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-1TB-Natural-Titanium/dp/B0DHTZP38"},
            {"retailer": "bestbuy", "price": 1599, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-16-pro-max-1tb-natural-titanium/MYWJ3LL-A"},
            {"retailer": "walmart", "price": 1599, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPhone-16-Pro-Max-1TB-Natural-Titanium/5000354048"},
            {"retailer": "bhphoto", "price": 1599, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800553-REG/apple_mywj3ll_a_iphone_16_pro_max_1tb.html"},
            {"retailer": "adorama", "price": 1599, "inStock": True, "url": "https://www.adorama.com/ac1tb16pmaxnt.html"}
        ],
        "releaseDate": "2024-09-20"
    },
    // iPhone 16 Pro 512GB
    {
        "id": "iphone-16-pro-512",
        "name": "iPhone 16 Pro",
        "category": "iphone",
        "specs": {"storage": "512GB", "color": "Natural Titanium", "display": "6.3\" Super Retina XDR", "camera": "48MP Fusion"},
        "prices": [
            {"retailer": "apple", "price": 1299, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-16-pro"},
            {"retailer": "amazon", "price": 1299, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-512GB-Natural-Titanium/dp/B0DHTZ25P"},
            {"retailer": "bestbuy", "price": 1299, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-16-pro-512gb-natural-titanium/MYMK3LL-A"},
            {"retailer": "walmart", "price": 1299, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPhone-16-Pro-512GB-Natural-Titanium/5000354037"},
            {"retailer": "bhphoto", "price": 1299, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800547-REG/apple_mymk3ll_a_iphone_16_pro_512gb.html"},
            {"retailer": "adorama", "price": 1299, "inStock": True, "url": "https://www.adorama.com/ac51216pnt.html"}
        ],
        "releaseDate": "2024-09-20"
    },
    // iPhone 16 and 16 Plus
    {
        "id": "iphone-16-128",
        "name": "iPhone 16",
        "category": "iphone",
        "specs": {"storage": "128GB", "color": "Ultramarine", "display": "6.1\" Super Retina XDR", "camera": "48MP Fusion"},
        "prices": [
            {"retailer": "apple", "price": 799, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-16"},
            {"retailer": "amazon", "price": 799, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-128GB-Ultramarine/dp/B0DHTYW7P8"},
            {"retailer": "bestbuy", "price": 799, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-16-128gb-ultramarine/MYAP3LL-A"},
            {"retailer": "walmart", "price": 799, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPhone-16-128GB-Ultramarine/5000354024"},
            {"retailer": "target", "price": 799, "inStock": True, "url": "https://www.target.com/p/apple-iphone-16/-/A-93597958"},
            {"retailer": "bhphoto", "price": 799, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800534-REG/apple_myap3ll_a_iphone_16_128gb.html"},
            {"retailer": "adorama", "price": 799, "inStock": True, "url": "https://www.adorama.com/ac12816um.html"}
        ],
        "releaseDate": "2024-09-20"
    },
    {
        "id": "iphone-16-plus-128",
        "name": "iPhone 16 Plus",
        "category": "iphone",
        "specs": {"storage": "128GB", "color": "Teal", "display": "6.7\" Super Retina XDR", "camera": "48MP Fusion"},
        "prices": [
            {"retailer": "apple", "price": 899, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-16"},
            {"retailer": "amazon", "price": 899, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-Plus-128GB-Teal/dp/B0DHTZ5XW"},
            {"retailer": "bestbuy", "price": 899, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-16-plus-128gb-teal/MXUT3LL-A"},
            {"retailer": "walmart", "price": 899, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPhone-16-Plus-128GB-Teal/5000354030"},
            {"retailer": "target", "price": 899, "inStock": True, "url": "https://www.target.com/p/apple-iphone-16-plus/-/A-93597959"},
            {"retailer": "bhphoto", "price": 899, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800538-REG/apple_mxut3ll_a_iphone_16_plus_128gb.html"},
            {"retailer": "adorama", "price": 899, "inStock": True, "url": "https://www.adorama.com/ac12816pt.html"}
        ],
        "releaseDate": "2024-09-20"
    },
    // iPhone 15 series (still current)
    {
        "id": "iphone-15-pro-max-256",
        "name": "iPhone 15 Pro Max",
        "category": "iphone",
        "specs": {"storage": "256GB", "color": "Natural Titanium", "display": "6.7\" Super Retina XDR", "camera": "48MP Pro"},
        "prices": [
            {"retailer": "apple", "price": 1099, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-15-pro"},
            {"retailer": "amazon", "price": 999, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-256GB-Natural-Titanium/dp/B0CHX1W1XY"},
            {"retailer": "bestbuy", "price": 999, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-15-pro-max-256gb-natural-titanium/MU663LL-A"},
            {"retailer": "walmart", "price": 999, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPhone-15-Pro-Max-256GB-Natural-Titanium/5063901321"},
            {"retailer": "bhphoto", "price": 999, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1782600-REG/apple_mu663ll_a_iphone_15_pro_max.html"},
            {"retailer": "adorama", "price": 999, "inStock": True, "url": "https://www.adorama.com/ac25615pmaxnt.html"}
        ],
        "releaseDate": "2023-09-22"
    },
    {
        "id": "iphone-15-pro-256",
        "name": "iPhone 15 Pro",
        "category": "iphone",
        "specs": {"storage": "256GB", "color": "Natural Titanium", "display": "6.1\" Super Retina XDR", "camera": "48MP Pro"},
        "prices": [
            {"retailer": "apple", "price": 999, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-15-pro"},
            {"retailer": "amazon", "price": 949, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-256GB-Natural-Titanium/dp/B0CHX4F374"},
            {"retailer": "bestbuy", "price": 949, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-15-pro-256gb-natural-titanium/MU6A3LL-A"},
            {"retailer": "walmart", "price": 949, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPhone-15-Pro-256GB-Natural-Titanium/5063901318"},
            {"retailer": "bhphoto", "price": 949, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1782594-REG/apple_mu6a3ll_a_iphone_15_pro_256gb.html"},
            {"retailer": "adorama", "price": 949, "inStock": True, "url": "https://www.adorama.com/ac25615pnt.html"}
        ],
        "releaseDate": "2023-09-22"
    },
    {
        "id": "iphone-15-128",
        "name": "iPhone 15",
        "category": "iphone",
        "specs": {"storage": "128GB", "color": "Pink", "display": "6.1\" Super Retina XDR", "camera": "48MP"},
        "prices": [
            {"retailer": "apple", "price": 699, "inStock": True, "url": "https://www.apple.com/shop/buy-iphone/iphone-15"},
            {"retailer": "amazon", "price": 649, "inStock": True, "url": "https://www.amazon.com/Apple-iPhone-128GB-Pink/dp/B0CHX2F9QT"},
            {"retailer": "bestbuy", "price": 649, "inStock": True, "url": "https://www.bestbuy.com/site/apple-iphone-15-128gb-pink/MTPN3LL-A"},
            {"retailer": "walmart", "price": 649, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPhone-15-128GB-Pink/5063901307"},
            {"retailer": "target", "price": 649, "inStock": True, "url": "https://www.target.com/p/apple-iphone-15/-/A-89345370"},
            {"retailer": "bhphoto", "price": 649, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1782574-REG/apple_mtpm3ll_a_iphone_15_128gb.html"},
            {"retailer": "adorama", "price": 649, "inStock": True, "url": "https://www.adorama.com/ac12815p.html"}
        ],
        "releaseDate": "2023-09-22"
    },
    // iPad Pro M4
    {
        "id": "ipad-pro-13-m4-256",
        "name": "iPad Pro 13\"",
        "category": "ipad",
        "specs": {"chip": "M4", "storage": "256GB", "display": "13\" Ultra Retina XDR", "color": "Space Black"},
        "prices": [
            {"retailer": "apple", "price": 1299, "inStock": True, "url": "https://www.apple.com/shop/buy-ipad/ipad-pro"},
            {"retailer": "amazon", "price": 1299, "inStock": True, "url": "https://www.amazon.com/Apple-iPad-Pro-13-inch-256GB/dp/B0D3J5Z9SX"},
            {"retailer": "bestbuy", "price": 1299, "inStock": True, "url": "https://www.bestbuy.com/site/apple-ipad-pro-13-inch-m4-chip-wi-fi-256gb-space-black/MVX23LL-A"},
            {"retailer": "walmart", "price": 1299, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPad-Pro-13-inch-M4-256GB-Wi-Fi-Space-Black/5038464532"},
            {"retailer": "bhphoto", "price": 1299, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1794196-REG/apple_mvx23ll_a_ipad_pro_13_m4_256gb.html"},
            {"retailer": "adorama", "price": 1299, "inStock": True, "url": "https://www.adorama.com/ac25613pm4sb.html"},
            {"retailer": "ebay", "price": 1199, "inStock": True, "url": "https://www.ebay.com/sch/i.html?_nkw=iPad+Pro+13+M4+256GB"}
        ],
        "releaseDate": "2024-05-15"
    },
    {
        "id": "ipad-pro-11-m4-256",
        "name": "iPad Pro 11\"",
        "category": "ipad",
        "specs": {"chip": "M4", "storage": "256GB", "display": "11\" Ultra Retina XDR", "color": "Silver"},
        "prices": [
            {"retailer": "apple", "price": 999, "inStock": True, "url": "https://www.apple.com/shop/buy-ipad/ipad-pro"},
            {"retailer": "amazon", "price": 999, "inStock": True, "url": "https://www.amazon.com/Apple-iPad-Pro-11-inch-256GB/dp/B0D3J6D5V8"},
            {"retailer": "bestbuy", "price": 999, "inStock": True, "url": "https://www.bestbuy.com/site/apple-ipad-pro-11-inch-m4-chip-wi-fi-256gb-silver/MVV93LL-A"},
            {"retailer": "walmart", "price": 999, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPad-Pro-11-inch-M4-256GB-Wi-Fi-Silver/5038464528"},
            {"retailer": "bhphoto", "price": 999, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1794193-REG/apple_mvv93ll_a_ipad_pro_11_m4_256gb.html"},
            {"retailer": "adorama", "price": 999, "inStock": True, "url": "https://www.adorama.com/ac25611pm4s.html"}
        ],
        "releaseDate": "2024-05-15"
    },
    // iPad Air M3
    {
        "id": "ipad-air-13-m3-256",
        "name": "iPad Air 13\"",
        "category": "ipad",
        "specs": {"chip": "M3", "storage": "256GB", "display": "13\" Liquid Retina", "color": "Space Gray"},
        "prices": [
            {"retailer": "apple", "price": 799, "inStock": True, "url": "https://www.apple.com/shop/buy-ipad/ipad-air"},
            {"retailer": "amazon", "price": 799, "inStock": True, "url": "https://www.amazon.com/Apple-iPad-Air-13-inch-256GB/dp/B0D3J3C1QD"},
            {"retailer": "bestbuy", "price": 799, "inStock": True, "url": "https://www.bestbuy.com/site/apple-ipad-air-13-inch-m3-chip-wi-fi-256gb-space-gray/MCNN4LL-A"},
            {"retailer": "walmart", "price": 799, "inStock": True, "url": "https://www.walmart.com/ip/Apple-13-inch-iPad-Air-M3-Wi-Fi-256GB-Space-Gray/5257747932"},
            {"retailer": "bhphoto", "price": 799, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1812269-REG/apple_mcnn4ll_a_ipad_air_13_m3_256gb.html"},
            {"retailer": "adorama", "price": 799, "inStock": True, "url": "https://www.adorama.com/ac25613m3sg.html"}
        ],
        "releaseDate": "2025-03-12"
    },
    {
        "id": "ipad-air-11-m3-256",
        "name": "iPad Air 11\"",
        "category": "ipad",
        "specs": {"chip": "M3", "storage": "256GB", "display": "11\" Liquid Retina", "color": "Blue"},
        "prices": [
            {"retailer": "apple", "price": 599, "inStock": True, "url": "https://www.apple.com/shop/buy-ipad/ipad-air"},
            {"retailer": "amazon", "price": 599, "inStock": True, "url": "https://www.amazon.com/Apple-iPad-Air-11-inch-256GB/dp/B0D3J5Z9SY"},
            {"retailer": "bestbuy", "price": 599, "inStock": True, "url": "https://www.bestbuy.com/site/apple-ipad-air-11-inch-m3-chip-wi-fi-256gb-blue/MCA14LL-A"},
            {"retailer": "walmart", "price": 599, "inStock": True, "url": "https://www.walmart.com/ip/Apple-11-inch-iPad-Air-M3-Wi-Fi-256GB-Blue/5257747928"},
            {"retailer": "bhphoto", "price": 599, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1812268-REG/apple_mca14ll_a_ipad_air_11_m3_256gb.html"},
            {"retailer": "adorama", "price": 599, "inStock": True, "url": "https://www.adorama.com/ac25611m3b.html"}
        ],
        "releaseDate": "2025-03-12"
    },
    // iPad mini 7
    {
        "id": "ipad-mini-7-128",
        "name": "iPad mini 7",
        "category": "ipad",
        "specs": {"chip": "A17 Pro", "storage": "128GB", "display": "8.3\" Liquid Retina", "color": "Starlight"},
        "prices": [
            {"retailer": "apple", "price": 499, "inStock": True, "url": "https://www.apple.com/shop/buy-ipad/ipad-mini"},
            {"retailer": "amazon", "price": 499, "inStock": True, "url": "https://www.amazon.com/Apple-iPad-mini-A17-Pro-128GB/dp/B0DKLHHMZ7"},
            {"retailer": "bestbuy", "price": 499, "inStock": True, "url": "https://www.bestbuy.com/site/apple-ipad-mini-7th-generation-a17-pro-chip-wi-fi-128gb-starlight/MXN63LL-A"},
            {"retailer": "walmart", "price": 499, "inStock": True, "url": "https://www.walmart.com/ip/Apple-iPad-mini-A17-Pro-128GB-Wi-Fi-Starlight/5257747936"},
            {"retailer": "bhphoto", "price": 499, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1807698-REG/apple_mxn63ll_a_ipad_mini_7_128gb.html"},
            {"retailer": "adorama", "price": 499, "inStock": True, "url": "https://www.adorama.com/ac128mini7s.html"}
        ],
        "releaseDate": "2024-10-23"
    },
    // MacBook Air M4
    {
        "id": "macbook-air-13-m4-24gb",
        "name": "MacBook Air 13\"",
        "category": "mac",
        "specs": {"chip": "M4", "ram": "24GB", "storage": "256GB SSD", "display": "13.6\" Liquid Retina", "color": "Midnight"},
        "prices": [
            {"retailer": "apple", "price": 1199, "inStock": True, "url": "https://www.apple.com/shop/buy-mac/macbook-air"},
            {"retailer": "amazon", "price": 1199, "inStock": True, "url": "https://www.amazon.com/Apple-MacBook-13-inch-10-Core-16-Core/dp/B0DKLHHMZ4"},
            {"retailer": "bestbuy", "price": 1199, "inStock": True, "url": "https://www.bestbuy.com/site/apple-macbook-air-13-inch-laptop-m4-chip-24gb-memory-256gb-ssd-midnight/MC654LL-A"},
            {"retailer": "walmart", "price": 1199, "inStock": True, "url": "https://www.walmart.com/ip/Apple-13-inch-MacBook-Air-M4-24GB-256GB-Midnight/15481367422"},
            {"retailer": "bhphoto", "price": 1199, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1811193-REG/apple_mc654ll_a_macbook_air_13_m4.html"},
            {"retailer": "adorama", "price": 1199, "inStock": True, "url": "https://www.adorama.com/acmba1324m4.html"}
        ],
        "releaseDate": "2025-03-12"
    },
    {
        "id": "macbook-air-15-m4-24gb",
        "name": "MacBook Air 15\"",
        "category": "mac",
        "specs": {"chip": "M4", "ram": "24GB", "storage": "256GB SSD", "display": "15.3\" Liquid Retina", "color": "Starlight"},
        "prices": [
            {"retailer": "apple", "price": 1399, "inStock": True, "url": "https://www.apple.com/shop/buy-mac/macbook-air"},
            {"retailer": "amazon", "price": 1399, "inStock": True, "url": "https://www.amazon.com/Apple-MacBook-15-inch-10-Core-16-Core/dp/B0DKLJ8X7L"},
            {"retailer": "bestbuy", "price": 1399, "inStock": True, "url": "https://www.bestbuy.com/site/apple-macbook-air-15-inch-laptop-m4-chip-24gb-memory-256gb-ssd-starlight/MC6J4LL-A"},
            {"retailer": "walmart", "price": 1399, "inStock": True, "url": "https://www.walmart.com/ip/Apple-15-inch-MacBook-Air-M4-24GB-256GB-Starlight/15481367423"},
            {"retailer": "bhphoto", "price": 1399, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1811196-REG/apple_mc6j4ll_a_macbook_air_15_m4.html"},
            {"retailer": "adorama", "price": 1399, "inStock": True, "url": "https://www.adorama.com/acmba1524m4.html"}
        ],
        "releaseDate": "2025-03-12"
    },
    // MacBook Pro M4
    {
        "id": "macbook-pro-16-m4-pro",
        "name": "MacBook Pro 16\"",
        "category": "mac",
        "specs": {"chip": "M4 Pro", "ram": "24GB", "storage": "512GB SSD", "display": "16.2\" Liquid Retina XDR", "color": "Space Black"},
        "prices": [
            {"retailer": "apple", "price": 2499, "inStock": True, "url": "https://www.apple.com/shop/buy-mac/macbook-pro"},
            {"retailer": "amazon", "price": 2499, "inStock": True, "url": "https://www.amazon.com/Apple-MacBook-16-inch-14-Core-20-Core/dp/B0DKLHHMZ6"},
            {"retailer": "bestbuy", "price": 2499, "inStock": True, "url": "https://www.bestbuy.com/site/apple-macbook-pro-16-inch-laptop-m4-pro-chip-24gb-memory-512gb-ssd-space-black/MX2X3LL-A"},
            {"retailer": "walmart", "price": 2499, "inStock": True, "url": "https://www.walmart.com/ip/Apple-16-inch-MacBook-Pro-M4-Pro-24GB-512GB-Space-Black/13679766553"},
            {"retailer": "bhphoto", "price": 2499, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1811197-REG/apple_mx2x3ll_a_macbook_pro_16_m4.html"},
            {"retailer": "adorama", "price": 2499, "inStock": True, "url": "https://www.adorama.com/acmbp1624m4p.html"}
        ],
        "releaseDate": "2024-11-08"
    },
    {
        "id": "macbook-pro-14-m4-pro",
        "name": "MacBook Pro 14\"",
        "category": "mac",
        "specs": {"chip": "M4 Pro", "ram": "24GB", "storage": "512GB SSD", "display": "14.2\" Liquid Retina XDR", "color": "Space Black"},
        "prices": [
            {"retailer": "apple", "price": 1999, "inStock": True, "url": "https://www.apple.com/shop/buy-mac/macbook-pro"},
            {"retailer": "amazon", "price": 1999, "inStock": True, "url": "https://www.amazon.com/Apple-MacBook-14-inch-14-Core-20-Core/dp/B0DKLHHMZ5"},
            {"retailer": "bestbuy", "price": 1999, "inStock": True, "url": "https://www.bestbuy.com/site/apple-macbook-pro-14-inch-laptop-m4-pro-chip-24gb-memory-512gb-ssd-space-black/MX2T3LL-A"},
            {"retailer": "walmart", "price": 1999, "inStock": True, "url": "https://www.walmart.com/ip/Apple-14-inch-MacBook-Pro-M4-Pro-24GB-512GB-Space-Black/13679766552"},
            {"retailer": "bhphoto", "price": 1999, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1811194-REG/apple_mx2t3ll_a_macbook_pro_14_m4.html"},
            {"retailer": "adorama", "price": 1999, "inStock": True, "url": "https://www.adorama.com/acmbp1424m4p.html"}
        ],
        "releaseDate": "2024-11-08"
    },
    {
        "id": "macbook-pro-14-m4",
        "name": "MacBook Pro 14\"",
        "category": "mac",
        "specs": {"chip": "M4", "ram": "16GB", "storage": "512GB SSD", "display": "14.2\" Liquid Retina XDR", "color": "Silver"},
        "prices": [
            {"retailer": "apple", "price": 1599, "inStock": True, "url": "https://www.apple.com/shop/buy-mac/macbook-pro"},
            {"retailer": "amazon", "price": 1599, "inStock": True, "url": "https://www.amazon.com/Apple-MacBook-14-inch-10-Core-10-Core/dp/B0DKLHH7T4"},
            {"retailer": "bestbuy", "price": 1599, "inStock": True, "url": "https://www.bestbuy.com/site/apple-macbook-pro-14-inch-laptop-m4-chip-16gb-memory-512gb-ssd-silver/MCX03LL-A"},
            {"retailer": "walmart", "price": 1599, "inStock": True, "url": "https://www.walmart.com/ip/Apple-14-inch-MacBook-Pro-M4-16GB-512GB-Silver/13679766551"},
            {"retailer": "bhphoto", "price": 1599, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1811195-REG/apple_mcx03ll_a_macbook_pro_14_m4.html"},
            {"retailer": "adorama", "price": 1599, "inStock": True, "url": "https://www.adorama.com/acmbp1416m4.html"}
        ],
        "releaseDate": "2024-11-08"
    },
    // Mac mini M4
    {
        "id": "mac-mini-m4-pro",
        "name": "Mac mini",
        "category": "mac",
        "specs": {"chip": "M4 Pro", "ram": "24GB", "storage": "512GB SSD", "color": "Silver"},
        "prices": [
            {"retailer": "apple", "price": 1399, "inStock": True, "url": "https://www.apple.com/shop/buy-mac/mac-mini"},
            {"retailer": "amazon", "price": 1399, "inStock": True, "url": "https://www.amazon.com/Apple-2024-Mac-Desktop-Computer/dp/B0DKLJ8X7M"},
            {"retailer": "bestbuy", "price": 1399, "inStock": True, "url": "https://www.bestbuy.com/site/apple-mac-mini-desktop-m4-pro-chip-24gb-memory-512gb-ssd-silver/MCX44LL-A"},
            {"retailer": "walmart", "price": 1399, "inStock": True, "url": "https://www.walmart.com/ip/Apple-2024-Mac-mini-Desktop-Computer-with-M4-Pro-chip-14-core-CPU-20-core-GPU-24GB-Unified-Memory-512GB/5406222930"},
            {"retailer": "bhphoto", "price": 1399, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1811196-REG/apple_mcx44ll_a_mac_mini_m4_pro.html"},
            {"retailer": "adorama", "price": 1399, "inStock": True, "url": "https://www.adorama.com/acmacminim4p.html"}
        ],
        "releaseDate": "2024-11-08"
    },
    // Apple Watch
    {
        "id": "apple-watch-ultra-2",
        "name": "Apple Watch Ultra 2",
        "category": "watch",
        "specs": {"size": "49mm", "case": "Natural Titanium", "band": "Orange Alpine Loop", "features": "GPS + Cellular"},
        "prices": [
            {"retailer": "apple", "price": 799, "inStock": True, "url": "https://www.apple.com/shop/buy-watch/apple-watch-ultra"},
            {"retailer": "amazon", "price": 749, "inStock": True, "url": "https://www.amazon.com/Apple-Watch-Ultra-2-GPS-Cellular/dp/B0CHX1W1XY"},
            {"retailer": "bestbuy", "price": 749, "inStock": True, "url": "https://www.bestbuy.com/site/apple-watch-ultra-2-gps-cellular-49mm-natural-titanium-case-with-orange-alpine-loop-medium/MQDY3LL-A"},
            {"retailer": "walmart", "price": 749, "inStock": True, "url": "https://www.walmart.com/ip/Apple-Watch-Ultra-2-GPS-Cellular-49mm-Natural-Titanium-Case-with-Orange-Alpine-Loop-Medium/5000354050"},
            {"retailer": "bhphoto", "price": 749, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800560-REG/apple_mqdy3ll_a_watch_ultra_2.html"},
            {"retailer": "adorama", "price": 749, "inStock": True, "url": "https://www.adorama.com/ac49u2oal.html"}
        ],
        "releaseDate": "2024-09-20"
    },
    {
        "id": "apple-watch-series-10-46mm",
        "name": "Apple Watch Series 10",
        "category": "watch",
        "specs": {"size": "46mm", "case": "Jet Black Aluminum", "band": "Black Sport Band", "features": "GPS"},
        "prices": [
            {"retailer": "apple", "price": 429, "inStock": True, "url": "https://www.apple.com/shop/buy-watch/apple-watch"},
            {"retailer": "amazon", "price": 399, "inStock": True, "url": "https://www.amazon.com/Apple-Watch-Series-10-GPS/dp/B0DGHQ72MX"},
            {"retailer": "bestbuy", "price": 399, "inStock": True, "url": "https://www.bestbuy.com/site/apple-watch-series-10-gps-46mm-jet-black-aluminum-case-with-black-sport-band-m-l/MXL83LL-A"},
            {"retailer": "walmart", "price": 399, "inStock": True, "url": "https://www.walmart.com/ip/Apple-Watch-Series-10-GPS-46mm-Jet-Black-Aluminum-Case-with-Black-Sport-Band-M-L/11385157009"},
            {"retailer": "target", "price": 399, "inStock": True, "url": "https://www.target.com/p/apple-watch-series-10-gps-46mm-jet-black-aluminum-case-with-black-sport-band-m-l/-/A-91122499"},
            {"retailer": "bhphoto", "price": 399, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800556-REG/apple_mxl83ll_a_watch_series_10.html"},
            {"retailer": "adorama", "price": 399, "inStock": True, "url": "https://www.adorama.com/ac46s10jb.html"}
        ],
        "releaseDate": "2024-09-20"
    },
    {
        "id": "apple-watch-se-44mm",
        "name": "Apple Watch SE 2nd Gen",
        "category": "watch",
        "specs": {"size": "44mm", "case": "Midnight Aluminum", "band": "Midnight Sport Band", "features": "GPS"},
        "prices": [
            {"retailer": "apple", "price": 249, "inStock": True, "url": "https://www.apple.com/shop/buy-watch/apple-watch-se"},
            {"retailer": "amazon", "price": 219, "inStock": True, "url": "https://www.amazon.com/Apple-Watch-SE-2nd-Generation/dp/B0DGHQ6F8X"},
            {"retailer": "bestbuy", "price": 219, "inStock": True, "url": "https://www.bestbuy.com/site/apple-watch-se-2nd-generation-gps-44mm-midnight-aluminum-case-with-midnight-sport-band-s-m/MXEK3LL-A"},
            {"retailer": "walmart", "price": 219, "inStock": True, "url": "https://www.walmart.com/ip/Apple-Watch-SE-2nd-Gen-GPS-44mm-Midnight-Aluminum-Case-with-Midnight-Sport-Band-S-M/11385157007"},
            {"retailer": "target", "price": 219, "inStock": True, "url": "https://www.target.com/p/apple-watch-se-2nd-generation-gps-44mm-midnight-aluminum-case-with-midnight-sport-band-s-m/-/A-91122497"},
            {"retailer": "bhphoto", "price": 219, "inStock": True, "url": "https://www.bhphotovideo.com/c/product/1800554-REG/apple_mxek3ll_a_watch_se_44mm.html"},
            {"retailer": "adorama", "price": 219, "inStock": True, "url": "https://www.adorama.com/ac44se2m.html"}
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