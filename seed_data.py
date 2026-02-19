"""
Seed data for Price Aggregator API
Creates sample products with Tier 1-2 fields
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Product, Retailer, Price
from datetime import datetime

def seed_retailers(db: Session):
    """Create sample retailers"""
    retailers = [
        {
            "name": "eBay",
            "base_url": "https://www.ebay.com",
            "scraper_type": "ebay",
            "config": {"rate_limit": 2.0}
        },
        {
            "name": "Reverb",
            "base_url": "https://reverb.com",
            "scraper_type": "reverb",
            "config": {"category": "music_gear"}
        },
        {
            "name": "PriceCharting",
            "base_url": "https://www.pricecharting.com",
            "scraper_type": "pricecharting",
            "config": {"categories": ["pokemon", "games"]}
        },
        {
            "name": "TCGPlayer",
            "base_url": "https://www.tcgplayer.com",
            "scraper_type": "tcgplayer",
            "config": {"categories": ["pokemon"]}
        }
    ]

    for r in retailers:
        existing = db.query(Retailer).filter(Retailer.name == r["name"]).first()
        if not existing:
            db.add(Retailer(**r))

    db.commit()
    print(f"✅ Seeded {len(retailers)} retailers")

def seed_mac_products(db: Session):
    """Create sample Mac products with Tier 2 fields"""
    products = [
        {
            "name": "MacBook Pro 14-inch M3 Pro",
            "category": "mac",
            "description": "2023 MacBook Pro with M3 Pro chip, Space Black",
            "model_identifier": "Mac15,3",
            "release_year": 2023,
            "specs": {
                "cpu": "Apple M3 Pro (11-core CPU, 14-core GPU)",
                "ram": "18GB Unified Memory",
                "storage": "512GB SSD",
                "display": "14.2-inch Liquid Retina XDR",
                "ports": ["3x Thunderbolt 4", "HDMI", "SD Card", "MagSafe 3"],
                "color": "Space Black"
            },
            "image_url": "https://example.com/macbook-pro-14.jpg"
        },
        {
            "name": "MacBook Air 15-inch M2",
            "category": "mac",
            "description": "2023 MacBook Air with M2 chip, Midnight",
            "model_identifier": "Mac14,2",
            "release_year": 2023,
            "specs": {
                "cpu": "Apple M2 (8-core CPU, 10-core GPU)",
                "ram": "8GB Unified Memory",
                "storage": "256GB SSD",
                "display": "15.3-inch Liquid Retina",
                "ports": ["2x Thunderbolt 3", "MagSafe 3", "Headphone Jack"],
                "color": "Midnight"
            },
            "image_url": "https://example.com/macbook-air-15.jpg"
        },
        {
            "name": "Mac mini M2 Pro",
            "category": "mac",
            "description": "Desktop Mac with M2 Pro chip",
            "model_identifier": "Mac14,12",
            "release_year": 2023,
            "specs": {
                "cpu": "Apple M2 Pro (10-core CPU, 16-core GPU)",
                "ram": "16GB Unified Memory",
                "storage": "512GB SSD",
                "ports": ["4x Thunderbolt 4", "2x USB-A", "HDMI", "Ethernet"]
            },
            "image_url": "https://example.com/mac-mini.jpg"
        }
    ]

    for p in products:
        existing = db.query(Product).filter(Product.name == p["name"]).first()
        if not existing:
            db.add(Product(**p))

    db.commit()
    print(f"✅ Seeded {len(products)} Mac products")

def seed_pokemon_products(db: Session):
    """Create sample Pokemon cards with Tier 2 fields"""
    products = [
        {
            "name": "Charizard EX",
            "category": "pokemon",
            "description": "Ultra Rare Charizard card from Scarlet & Violet set",
            "set_name": "Scarlet & Violet",
            "card_number": "125/198",
            "rarity": "Ultra Rare",
            "condition": "NM",
            "image_url": "https://example.com/charizard-ex.jpg"
        },
        {
            "name": "Pikachu VMAX",
            "category": "pokemon",
            "description": "Rainbow Rare Pikachu from Vivid Voltage",
            "set_name": "Vivid Voltage",
            "card_number": "188/185",
            "rarity": "Secret Rare",
            "condition": "NM",
            "image_url": "https://example.com/pikachu-vmax.jpg"
        },
        {
            "name": "Mewtwo V",
            "category": "pokemon",
            "description": "Holo Rare Mewtwo from Pokemon GO set",
            "set_name": "Pokemon GO",
            "card_number": "072/078",
            "rarity": "Holo Rare",
            "condition": "LP",
            "image_url": "https://example.com/mewtwo-v.jpg"
        }
    ]

    for p in products:
        existing = db.query(Product).filter(Product.name == p["name"]).first()
        if not existing:
            db.add(Product(**p))

    db.commit()
    print(f"✅ Seeded {len(products)} Pokemon cards")

def seed_audio_products(db: Session):
    """Create sample audio gear with Tier 2 fields"""
    products = [
        {
            "name": "Fender American Professional II Stratocaster",
            "category": "audio",
            "description": "Professional electric guitar with V-Mod II pickups",
            "brand": "Fender",
            "model": "American Professional II Stratocaster",
            "image_url": "https://example.com/fender-strat.jpg"
        },
        {
            "name": "Shure SM7B",
            "category": "audio",
            "description": "Professional dynamic microphone for broadcast and podcasting",
            "brand": "Shure",
            "model": "SM7B",
            "image_url": "https://example.com/shure-sm7b.jpg"
        },
        {
            "name": "Focusrite Scarlett 2i2 3rd Gen",
            "category": "audio",
            "description": "USB audio interface with 2 inputs/outputs",
            "brand": "Focusrite",
            "model": "Scarlett 2i2 Gen 3",
            "image_url": "https://example.com/focusrite-2i2.jpg"
        }
    ]

    for p in products:
        existing = db.query(Product).filter(Product.name == p["name"]).first()
        if not existing:
            db.add(Product(**p))

    db.commit()
    print(f"✅ Seeded {len(products)} audio products")

def seed_sample_prices(db: Session):
    """Create sample prices for products"""
    retailers = db.query(Retailer).all()
    products = db.query(Product).all()

    if not retailers or not products:
        print("⚠️  Need retailers and products first")
        return

    sample_prices = [
        # Mac prices
        {"product_name": "MacBook Pro 14-inch M3 Pro", "price": 1999.00, "condition": "new"},
        {"product_name": "MacBook Pro 14-inch M3 Pro", "price": 1749.00, "condition": "used"},
        {"product_name": "MacBook Air 15-inch M2", "price": 1299.00, "condition": "new"},
        {"product_name": "Mac mini M2 Pro", "price": 1299.00, "condition": "new"},

        # Pokemon prices
        {"product_name": "Charizard EX", "price": 45.00, "condition": "NM"},
        {"product_name": "Charizard EX", "price": 32.00, "condition": "LP"},
        {"product_name": "Pikachu VMAX", "price": 120.00, "condition": "NM"},
        {"product_name": "Mewtwo V", "price": 8.50, "condition": "LP"},

        # Audio prices
        {"product_name": "Fender American Professional II Stratocaster", "price": 1599.00, "condition": "new"},
        {"product_name": "Shure SM7B", "price": 399.00, "condition": "new"},
        {"product_name": "Focusrite Scarlett 2i2 3rd Gen", "price": 169.99, "condition": "new"},
    ]

    count = 0
    for sp in sample_prices:
        product = db.query(Product).filter(Product.name == sp["product_name"]).first()
        if product:
            for retailer in retailers[:2]:  # Add prices from first 2 retailers
                existing = db.query(Price).filter(
                    Price.product_id == product.id,
                    Price.retailer_id == retailer.id
                ).first()

                if not existing:
                    db.add(Price(
                        product_id=product.id,
                        retailer_id=retailer.id,
                        price=sp["price"] * (0.9 if retailer.name == "eBay" else 1.0),
                        condition=sp["condition"],
                        listing_url=f"https://{retailer.name.lower()}.com/listing/{product.id}",
                        listing_title=product.name
                    ))
                    count += 1

    db.commit()
    print(f"✅ Seeded {count} sample prices")

def main():
    """Run all seed functions"""
    print("🌱 Seeding database...")

    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_retailers(db)
        seed_mac_products(db)
        seed_pokemon_products(db)
        seed_audio_products(db)
        seed_sample_prices(db)

        print("\n✅ Database seeded successfully!")
        print("\nSample data created:")
        print("  - 4 Retailers (eBay, Reverb, PriceCharting, TCGPlayer)")
        print("  - 3 Mac products (with specs)")
        print("  - 3 Pokemon cards (with set/rarity)")
        print("  - 3 Audio products (with brand/model)")
        print("  - Sample prices for comparison")

    except Exception as e:
        print(f"❌ Error seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
