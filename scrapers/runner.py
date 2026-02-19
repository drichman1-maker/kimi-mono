"""
Scraper Runner and Scheduler
"""

import schedule
import time
import threading
from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Product, Retailer, Price
from app.services.scraper_service import ScraperService

class ScraperRunner:
    """Manages and runs scrapers on schedule"""

    def __init__(self):
        self.jobs = []
        self.running = False
        self.thread = None

    def register_scraper(self, scraper_class, retailer_id: int, interval_minutes: int = 60):
        """Register a scraper to run on schedule"""
        def job():
            db = SessionLocal()
            try:
                retailer = db.query(Retailer).filter(Retailer.id == retailer_id).first()
                if not retailer or not retailer.is_active:
                    return

                scraper = scraper_class(retailer_id, retailer.base_url)
                service = ScraperService(db)

                print(f"[{datetime.now()}] Running {retailer.name} scraper...")

                # Get products to scrape
                products = db.query(Product).filter(Product.is_active == True).all()

                for product in products[:10]:  # Limit to prevent overload
                    try:
                        results = scraper.search(product.name, category=product.category)

                        prices = []
                        for result in results[:3]:  # Top 3 results
                            prices.append({
                                'retailer_id': retailer_id,
                                'price': result['price'],
                                'condition': result.get('condition', 'unknown'),
                                'listing_url': result.get('url'),
                                'listing_title': result['name'][:500]
                            })

                        if prices:
                            service.process_scraped_data(
                                {
                                    'name': product.name,
                                    'category': product.category,
                                    'description': product.description,
                                    'image_url': product.image_url
                                },
                                prices
                            )

                        scraper.rate_limit(2, 5)  # Be nice to servers

                    except Exception as e:
                        print(f"Error scraping {product.name}: {e}")

                print(f"[{datetime.now()}] Completed {retailer.name} scraper")

            finally:
                db.close()

        schedule.every(interval_minutes).minutes.do(job)
        self.jobs.append({
            'retailer_id': retailer_id,
            'interval': interval_minutes,
            'scraper': scraper_class.__name__
        })

    def start(self):
        """Start the scheduler in background thread"""
        if self.running:
            return

        self.running = True

        def run_schedule():
            while self.running:
                schedule.run_pending()
                time.sleep(1)

        self.thread = threading.Thread(target=run_schedule, daemon=True)
        self.thread.start()
        print(f"✅ Scraper scheduler started with {len(self.jobs)} jobs")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        schedule.clear()
        print("🛑 Scraper scheduler stopped")

    def get_status(self) -> Dict:
        """Get scheduler status"""
        return {
            'running': self.running,
            'jobs': self.jobs,
            'next_run': str(schedule.next_run()) if schedule.next_run() else None
        }

# Manual scraper execution
def run_scraper_now(retailer_id: int, product_query: str = None):
    """Run a scraper immediately (for testing)"""
    db = SessionLocal()
    try:
        from scrapers.tier1_2_scrapers import eBayScraper, ReverbScraper, PriceChartingScraper

        retailer = db.query(Retailer).filter(Retailer.id == retailer_id).first()
        if not retailer:
            return {"error": "Retailer not found"}

        # Select scraper based on type
        scraper_map = {
            'ebay': eBayScraper,
            'reverb': ReverbScraper,
            'pricecharting': PriceChartingScraper
        }

        scraper_class = scraper_map.get(retailer.scraper_type)
        if not scraper_class:
            return {"error": f"Unknown scraper type: {retailer.scraper_type}"}

        scraper = scraper_class(retailer_id, retailer.base_url)

        # Search
        query = product_query or "MacBook Pro"
        results = scraper.search(query)

        return {
            "retailer": retailer.name,
            "query": query,
            "results_found": len(results),
            "results": results[:5]  # Return first 5
        }

    finally:
        db.close()

# Initialize and start
def init_scheduler():
    """Initialize scheduler with configured retailers"""
    runner = ScraperRunner()

    db = SessionLocal()
    try:
        retailers = db.query(Retailer).filter(Retailer.is_active == True).all()

        for retailer in retailers:
            from scrapers.tier1_2_scrapers import eBayScraper, ReverbScraper, PriceChartingScraper

            scraper_map = {
                'ebay': eBayScraper,
                'reverb': ReverbScraper,
                'pricecharting': PriceChartingScraper
            }

            scraper_class = scraper_map.get(retailer.scraper_type)
            if scraper_class:
                runner.register_scraper(scraper_class, retailer.id, interval_minutes=60)

    finally:
        db.close()

    return runner
