"""
Base Scraper Class
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import time
import random

class BaseScraper(ABC):
    """Abstract base class for all scrapers"""

    def __init__(self, retailer_id: int, base_url: str):
        self.retailer_id = retailer_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    @abstractmethod
    def search(self, query: str, **kwargs) -> List[Dict]:
        """Search for products"""
        pass

    @abstractmethod
    def get_product_details(self, product_url: str) -> Dict:
        """Get detailed product information"""
        pass

    @abstractmethod
    def parse_price(self, price_text: str) -> float:
        """Extract numeric price from text"""
        pass

    def fetch(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """Fetch and parse URL with retry logic"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(1, 3))
        return None

    def rate_limit(self, min_delay: float = 1.0, max_delay: float = 3.0):
        """Rate limiting to be nice to servers"""
        time.sleep(random.uniform(min_delay, max_delay))

class GenericScraper(BaseScraper):
    """Generic scraper for standard e-commerce sites"""

    def search(self, query: str, **kwargs) -> List[Dict]:
        """Generic search implementation"""
        search_url = f"{self.base_url}/search?q={query.replace(' ', '+')}"
        soup = self.fetch(search_url)

        if not soup:
            return []

        results = []
        # Generic selectors - should be overridden
        items = soup.select('.product-item') or soup.select('.search-result')

        for item in items[:10]:  # Limit to 10 results
            try:
                title_elem = item.select_one('.product-title, .title, h2, h3')
                price_elem = item.select_one('.price, .cost, .amount')
                link_elem = item.select_one('a[href]')

                if title_elem and price_elem:
                    results.append({
                        'name': title_elem.get_text(strip=True),
                        'price': self.parse_price(price_elem.get_text()),
                        'url': link_elem['href'] if link_elem else None,
                        'condition': 'new'
                    })
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue

        return results

    def get_product_details(self, product_url: str) -> Dict:
        """Generic product details"""
        if not product_url.startswith('http'):
            product_url = self.base_url + product_url

        soup = self.fetch(product_url)
        if not soup:
            return {}

        return {
            'title': soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else '',
            'description': soup.select_one('.description, #description').get_text(strip=True) if soup.select_one('.description, #description') else '',
            'image': soup.select_one('img.product-image, .main-image img')['src'] if soup.select_one('img.product-image, .main-image img') else None
        }

    def parse_price(self, price_text: str) -> float:
        """Extract price from text"""
        import re
        # Remove currency symbols and whitespace
        cleaned = re.sub(r'[^\d.,]', '', price_text)
        # Handle European format (1.234,56)
        if ',' in cleaned and '.' in cleaned:
            if cleaned.rfind(',') > cleaned.rfind('.'):
                cleaned = cleaned.replace('.', '').replace(',', '.')
            else:
                cleaned = cleaned.replace(',', '')
        elif ',' in cleaned:
            cleaned = cleaned.replace(',', '.')

        try:
            return float(cleaned)
        except ValueError:
            return 0.0
