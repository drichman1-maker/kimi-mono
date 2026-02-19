"""
Pokemon Card Scrapers
"""

from typing import List, Dict
from scrapers.base import BaseScraper
import re

class PriceChartingScraper(BaseScraper):
    """Scraper for PriceCharting.com"""

    def search(self, query: str, **kwargs) -> List[Dict]:
        """Search Pokemon cards"""
        search_url = f"{self.base_url}/search?q={query.replace(' ', '+')}"
        soup = self.fetch(search_url)

        if not soup:
            return []

        results = []
        items = soup.select('.search-result, .product-card')

        for item in items:
            try:
                title = item.select_one('.title, h3, .product-title')
                price = item.select_one('.price, .current-price')
                set_name = item.select_one('.set-name, .category')

                if title:
                    results.append({
                        'name': title.get_text(strip=True),
                        'price': self.parse_price(price.get_text()) if price else 0,
                        'set_name': set_name.get_text(strip=True) if set_name else None,
                        'category': 'pokemon'
                    })
            except Exception as e:
                print(f"Error: {e}")

        return results

    def get_product_details(self, product_url: str) -> Dict:
        """Get card details"""
        soup = self.fetch(product_url)
        if not soup:
            return {}

        # Extract card number and rarity
        card_info = soup.select_one('.card-info, .product-info')
        card_number = None
        rarity = None

        if card_info:
            text = card_info.get_text()
            num_match = re.search(r'#?(\d+)/\d+', text)
            if num_match:
                card_number = num_match.group(0)

            rarity_patterns = ['Common', 'Uncommon', 'Rare', 'Holo', 'Secret', 'Ultra']
            for pattern in rarity_patterns:
                if pattern in text:
                    rarity = pattern
                    break

        return {
            'name': soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else '',
            'card_number': card_number,
            'rarity': rarity,
            'set_name': self._extract_set_name(soup),
            'category': 'pokemon'
        }

    def _extract_set_name(self, soup) -> str:
        """Extract set name"""
        set_elem = soup.select_one('.set-name, .series-name, a[href*="/set/"]')
        return set_elem.get_text(strip=True) if set_elem else ''

    def parse_price(self, price_text: str) -> float:
        """Parse price"""
        import re
        match = re.search(r'\$([\d,]+(?:\.\d{2})?)', price_text)
        if match:
            return float(match.group(1).replace(',', ''))
        return 0.0

class TCGPlayerScraper(BaseScraper):
    """Scraper for TCGPlayer.com"""

    def search(self, query: str, **kwargs) -> List[Dict]:
        """Search TCGPlayer"""
        search_url = f"{self.base_url}/search?q={query.replace(' ', '+')}"
        soup = self.fetch(search_url)

        if not soup:
            return []

        results = []
        items = soup.select('.search-item, .product-card')

        for item in items:
            try:
                title = item.select_one('.product-name, h3, .title')
                price = item.select_one('.market-price, .price')

                if title:
                    results.append({
                        'name': title.get_text(strip=True),
                        'price': self.parse_price(price.get_text()) if price else 0,
                        'category': 'pokemon'
                    })
            except Exception as e:
                print(f"Error: {e}")

        return results

    def get_product_details(self, product_url: str) -> Dict:
        """Get card details from TCGPlayer"""
        soup = self.fetch(product_url)
        if not soup:
            return {}

        return {
            'name': soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else '',
            'set_name': self._extract_set(soup),
            'rarity': self._extract_rarity(soup),
            'category': 'pokemon'
        }

    def _extract_set(self, soup) -> str:
        """Extract set name"""
        set_elem = soup.select_one('.set-name, [data-testid="set-name"]')
        return set_elem.get_text(strip=True) if set_elem else ''

    def _extract_rarity(self, soup) -> str:
        """Extract rarity"""
        rarity_elem = soup.select_one('.rarity, [data-testid="rarity"]')
        return rarity_elem.get_text(strip=True) if rarity_elem else ''

    def parse_price(self, price_text: str) -> float:
        """Parse TCGPlayer price"""
        import re
        match = re.search(r'\$([\d,]+(?:\.\d{2})?)', price_text)
        if match:
            return float(match.group(1).replace(',', ''))
        return 0.0
