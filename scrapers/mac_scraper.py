"""
Mac/Apple Product Scrapers
"""

from typing import List, Dict
from scrapers.base import BaseScraper
import re

class EveryMacScraper(BaseScraper):
    """Scraper for EveryMac.com specifications"""

    def search(self, query: str, **kwargs) -> List[Dict]:
        """Search EveryMac database"""
        search_url = f"{self.base_url}/search/?q={query.replace(' ', '+')}"
        soup = self.fetch(search_url)

        if not soup:
            return []

        results = []
        items = soup.select('.result-item, .search-result')

        for item in items:
            try:
                title = item.select_one('h2, h3, .title')
                specs = item.select_one('.specs, .details')
                link = item.select_one('a[href]')

                if title:
                    results.append({
                        'name': title.get_text(strip=True),
                        'specs': specs.get_text(strip=True) if specs else '',
                        'url': link['href'] if link else None,
                        'category': 'mac'
                    })
            except Exception as e:
                print(f"Error: {e}")

        return results

    def get_product_details(self, product_url: str) -> Dict:
        """Get Mac specs from EveryMac"""
        soup = self.fetch(product_url)
        if not soup:
            return {}

        specs = {}
        spec_rows = soup.select('table.specs tr, .specification-row')

        for row in spec_rows:
            cells = row.select('td, th')
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True).lower().replace(' ', '_')
                value = cells[1].get_text(strip=True)
                specs[key] = value

        # Extract model identifier
        model_id = None
        for key in ['model_identifier', 'identifier', 'model_no']:
            if key in specs:
                model_id = specs[key]
                break

        return {
            'specs': specs,
            'model_identifier': model_id,
            'release_year': self._extract_year(specs.get('intro_date', '')),
            'category': 'mac'
        }

    def _extract_year(self, date_text: str) -> int:
        """Extract year from date text"""
        match = re.search(r'20\d{2}', date_text)
        return int(match.group()) if match else None

    def parse_price(self, price_text: str) -> float:
        """Parse price (EveryMac doesn't have prices, but implement for consistency)"""
        return 0.0

class AppleStoreScraper(BaseScraper):
    """Scraper for Apple Store (educational/fair use)"""

    def search(self, query: str, **kwargs) -> List[Dict]:
        """Search Apple Store"""
        search_url = f"{self.base_url}/search/{query.replace(' ', '%20')}"
        soup = self.fetch(search_url)

        if not soup:
            return []

        results = []
        items = soup.select('.rf-hcard-copy, .rf-hcard-copy-title')

        for item in items:
            try:
                title = item.get_text(strip=True)
                price_elem = item.find_next(text=re.compile(r'\$[\d,]+'))

                price = 0
                if price_elem:
                    price = self.parse_price(price_elem)

                results.append({
                    'name': title,
                    'price': price,
                    'condition': 'new',
                    'category': 'mac'
                })
            except Exception as e:
                print(f"Error: {e}")

        return results

    def get_product_details(self, product_url: str) -> Dict:
        """Get Apple product details"""
        soup = self.fetch(product_url)
        if not soup:
            return {}

        return {
            'name': soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else '',
            'description': soup.select_one('.description').get_text(strip=True) if soup.select_one('.description') else '',
            'specs': self._extract_specs(soup),
            'category': 'mac'
        }

    def _extract_specs(self, soup) -> Dict:
        """Extract technical specifications"""
        specs = {}
        spec_sections = soup.select('.tech-specs, .specs-section')

        for section in spec_sections:
            rows = section.select('tr, .spec-row')
            for row in rows:
                key_elem = row.select_one('th, .spec-label')
                val_elem = row.select_one('td, .spec-value')

                if key_elem and val_elem:
                    key = key_elem.get_text(strip=True).lower().replace(' ', '_')
                    specs[key] = val_elem.get_text(strip=True)

        return specs

    def parse_price(self, price_text: str) -> float:
        """Parse Apple price format"""
        import re
        match = re.search(r'\$([\d,]+(?:\.\d{2})?)', price_text)
        if match:
            return float(match.group(1).replace(',', ''))
        return 0.0

class MacSalesScraper(BaseScraper):
    """Scraper for OWC MacSales (used/refurbished Macs)"""

    def search(self, query: str, **kwargs) -> List[Dict]:
        """Search MacSales inventory"""
        search_url = f"{self.base_url}/search?keyword={query.replace(' ', '+')}"
        soup = self.fetch(search_url)

        if not soup:
            return []

        results = []
        items = soup.select('.product-item, .product-list-item')

        for item in items:
            try:
                title = item.select_one('.product-title, h2, h3')
                price = item.select_one('.price, .product-price')
                link = item.select_one('a[href]')

                if title and price:
                    results.append({
                        'name': title.get_text(strip=True),
                        'price': self.parse_price(price.get_text()),
                        'url': link['href'] if link else None,
                        'condition': 'used',
                        'category': 'mac'
                    })
            except Exception as e:
                print(f"Error: {e}")

        return results

    def get_product_details(self, product_url: str) -> Dict:
        """Get product details from MacSales"""
        soup = self.fetch(product_url)
        if not soup:
            return {}

        return {
            'name': soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else '',
            'description': soup.select_one('.description').get_text(strip=True) if soup.select_one('.description') else '',
            'specs': self._extract_specs(soup),
            'category': 'mac'
        }

    def _extract_specs(self, soup) -> Dict:
        """Extract Mac specs"""
        specs = {}
        rows = soup.select('.specs-table tr, .product-specs li')

        for row in rows:
            text = row.get_text(strip=True)
            if ':' in text:
                key, value = text.split(':', 1)
                specs[key.strip().lower().replace(' ', '_')] = value.strip()

        return specs

    def parse_price(self, price_text: str) -> float:
        """Parse price"""
        import re
        match = re.search(r'\$([\d,]+(?:\.\d{2})?)', price_text)
        if match:
            return float(match.group(1).replace(',', ''))
        return 0.0
