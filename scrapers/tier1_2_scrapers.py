"""
Tier 1-2 Scraper Implementations
Supports: eBay, PriceCharting, Reverb
"""

from typing import List, Dict, Optional
from scrapers.base import BaseScraper
import re
from urllib.parse import quote_plus

class eBayScraper(BaseScraper):
    """eBay scraper with Tier 1-2 field extraction"""

    def __init__(self, retailer_id: int, base_url: str = "https://www.ebay.com"):
        super().__init__(retailer_id, base_url)
        self.api_url = "https://www.ebay.com/sch/i.html"

    def search(self, query: str, **kwargs) -> List[Dict]:
        """
        Search eBay with filters
        kwargs: category, condition, min_price, max_price
        """
        params = {
            '_nkw': query,
            '_sacat': kwargs.get('category', '0')
        }

        # Add condition filter
        condition = kwargs.get('condition')
        if condition == 'new':
            params['LH_ItemCondition'] = '1000'
        elif condition == 'used':
            params['LH_ItemCondition'] = '3000'

        # Add price filters
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        if min_price or max_price:
            params['_udlo'] = min_price
            params['_udhi'] = max_price

        search_url = f"{self.api_url}?{'&'.join([f'{k}={quote_plus(str(v))}' for k, v in params.items()])}"
        soup = self.fetch(search_url)

        if not soup:
            return []

        results = []
        items = soup.select('.s-item') or soup.select('[data-view="mi:1686|iid:1"]')

        for item in items:
            try:
                # Skip the "Shop on eBay" placeholder
                title_elem = item.select_one('.s-item__title, .s-item__title--has-tags')
                if not title_elem or 'Shop on eBay' in title_elem.get_text():
                    continue

                price_elem = item.select_one('.s-item__price')
                link_elem = item.select_one('.s-item__link')
                subtitle = item.select_one('.s-item__subtitle')
                shipping = item.select_one('.s-item__shipping')
                seller = item.select_one('.s-item__seller-info-text')

                title = title_elem.get_text(strip=True)
                price_text = price_elem.get_text(strip=True) if price_elem else '$0.00'

                # Determine condition from subtitle or title
                item_condition = 'unknown'
                subtitle_text = subtitle.get_text(strip=True).lower() if subtitle else ''
                if 'new' in subtitle_text or 'brand new' in title.lower():
                    item_condition = 'new'
                elif 'used' in subtitle_text or 'pre-owned' in subtitle_text:
                    item_condition = 'used'
                elif 'refurbished' in subtitle_text:
                    item_condition = 'refurbished'

                results.append({
                    'name': title,
                    'price': self.parse_price(price_text),
                    'url': link_elem['href'] if link_elem else None,
                    'condition': item_condition,
                    'shipping': self.parse_price(shipping.get_text()) if shipping else 0,
                    'seller': seller.get_text(strip=True) if seller else 'Unknown',
                    'category': kwargs.get('product_category', 'other')
                })

            except Exception as e:
                print(f"Error parsing eBay item: {e}")
                continue

        return results

    def get_product_details(self, product_url: str) -> Dict:
        """Extract detailed product info from eBay listing"""
        soup = self.fetch(product_url)
        if not soup:
            return {}

        # Extract specifications table
        specs = {}
        spec_tables = soup.select('.itemAttr, .prodDetailSec')
        for table in spec_tables:
            rows = table.select('tr')
            for row in rows:
                cells = row.select('td, th')
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True).rstrip(':').lower().replace(' ', '_')
                    value = cells[1].get_text(strip=True)
                    specs[key] = value

        # Extract images
        images = []
        img_elems = soup.select('.fs_imgc img, #icImg')
        for img in img_elems:
            src = img.get('src') or img.get('data-src')
            if src:
                images.append(src)

        return {
            'name': soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else '',
            'description': soup.select_one('#desc_wrapper, .item-description').get_text(strip=True) if soup.select_one('#desc_wrapper, .item-description') else '',
            'specs': specs,
            'images': images,
            'condition': specs.get('condition', 'unknown'),
            'category': 'other'
        }

    def parse_price(self, price_text: str) -> float:
        """Parse eBay price format"""
        import re
        # Handle ranges like "$100.00 to $150.00" - take the lower
        if 'to' in price_text.lower():
            price_text = price_text.split('to')[0]

        match = re.search(r'\$([\d,]+(?:\.\d{2})?)', price_text)
        if match:
            return float(match.group(1).replace(',', ''))
        return 0.0

    def search_mac_products(self, model: str, year: Optional[int] = None) -> List[Dict]:
        """Specialized search for Mac products with Tier 2 fields"""
        query = f"MacBook {model}"
        if year:
            query += f" {year}"

        results = self.search(query, category="111422", product_category="mac")

        # Enrich with Mac-specific Tier 2 fields
        for result in results:
            result['tier2_fields'] = {
                'model_identifier': self._extract_model_id(result['name']),
                'release_year': self._extract_year(result['name']),
                'specs': self._extract_mac_specs(result['name'])
            }

        return results

    def search_pokemon_cards(self, card_name: str, set_name: Optional[str] = None) -> List[Dict]:
        """Specialized search for Pokemon cards"""
        query = f"Pokemon {card_name}"
        if set_name:
            query += f" {set_name}"

        results = self.search(query, category="183454", product_category="pokemon")

        # Enrich with Pokemon-specific Tier 2 fields
        for result in results:
            result['tier2_fields'] = {
                'set_name': set_name or self._extract_set_name(result['name']),
                'card_number': self._extract_card_number(result['name']),
                'rarity': self._extract_rarity(result['name']),
                'condition': result.get('condition', 'unknown')
            }

        return results

    def _extract_model_id(self, text: str) -> Optional[str]:
        """Extract Mac model identifier"""
        patterns = [
            r'Mac\d+,\d+',
            r'MacBookPro\d+,\d+',
            r'MacBookAir\d+,\d+'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None

    def _extract_year(self, text: str) -> Optional[int]:
        """Extract year from text"""
        match = re.search(r'20(\d{2})', text)
        return 2000 + int(match.group(1)) if match else None

    def _extract_mac_specs(self, text: str) -> Dict:
        """Extract Mac specs from title"""
        specs = {}

        # Screen size
        size_match = re.search(r'(\d{2}(?:\.\d)?)\s*"', text)
        if size_match:
            specs['screen_size'] = size_match.group(1) + '"'

        # CPU
        if 'M1' in text:
            specs['cpu'] = 'Apple M1'
        elif 'M2' in text:
            specs['cpu'] = 'Apple M2'
        elif 'M3' in text:
            specs['cpu'] = 'Apple M3'
        elif 'Intel' in text:
            specs['cpu'] = 'Intel'

        # RAM
        ram_match = re.search(r'(\d+)\s*GB', text)
        if ram_match:
            specs['ram'] = ram_match.group(1) + 'GB'

        return specs

    def _extract_set_name(self, text: str) -> Optional[str]:
        """Extract Pokemon set name"""
        common_sets = ['Base Set', 'Jungle', 'Fossil', 'Team Rocket', 'Neo Genesis',
                      'Expedition', 'Ruby & Sapphire', 'Diamond & Pearl', 'Plasma Storm',
                      'XY', 'Sun & Moon', 'Sword & Shield', 'Scarlet & Violet']

        for set_name in common_sets:
            if set_name.lower() in text.lower():
                return set_name
        return None

    def _extract_card_number(self, text: str) -> Optional[str]:
        """Extract card number"""
        match = re.search(r'#?(\d+)/\d+', text)
        return match.group(0) if match else None

    def _extract_rarity(self, text: str) -> Optional[str]:
        """Extract rarity"""
        rarities = ['Common', 'Uncommon', 'Rare', 'Holo Rare', 'Ultra Rare', 
                   'Secret Rare', 'Rainbow Rare', 'Gold Rare', 'Full Art']

        for rarity in rarities:
            if rarity.lower() in text.lower():
                return rarity
        return None

class ReverbScraper(BaseScraper):
    """Reverb.com scraper for audio/music gear"""

    def __init__(self, retailer_id: int, base_url: str = "https://reverb.com"):
        super().__init__(retailer_id, base_url)

    def search(self, query: str, **kwargs) -> List[Dict]:
        """Search Reverb for music gear"""
        search_url = f"{self.base_url}/marketplace?query={quote_plus(query)}"

        # Add category filter
        category = kwargs.get('category')
        if category:
            search_url += f"&category={category}"

        soup = self.fetch(search_url)
        if not soup:
            return []

        results = []
        items = soup.select('.grid-card', ) or soup.select('[data-testid="listing-card"]')

        for item in items:
            try:
                title = item.select_one('.grid-card__title, h2, h3')
                price = item.select_one('.grid-card__price, .price')
                condition = item.select_one('.condition-label, .condition')
                link = item.select_one('a[href]')

                if title and price:
                    results.append({
                        'name': title.get_text(strip=True),
                        'price': self.parse_price(price.get_text()),
                        'url': self.base_url + link['href'] if link and link['href'].startswith('/') else link.get('href'),
                        'condition': condition.get_text(strip=True).lower() if condition else 'used',
                        'category': 'audio'
                    })
            except Exception as e:
                print(f"Error parsing Reverb item: {e}")

        return results

    def get_product_details(self, product_url: str) -> Dict:
        """Get product details from Reverb"""
        soup = self.fetch(product_url)
        if not soup:
            return {}

        # Extract brand and model
        brand = soup.select_one('.brand, [data-testid="brand"]')
        model = soup.select_one('.model, [data-testid="model"]')

        return {
            'name': soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else '',
            'brand': brand.get_text(strip=True) if brand else '',
            'model': model.get_text(strip=True) if model else '',
            'description': soup.select_one('.description').get_text(strip=True) if soup.select_one('.description') else '',
            'category': 'audio'
        }

    def parse_price(self, price_text: str) -> float:
        """Parse Reverb price"""
        import re
        match = re.search(r'\$([\d,]+(?:\.\d{2})?)', price_text)
        if match:
            return float(match.group(1).replace(',', ''))
        return 0.0

    def search_by_brand(self, brand: str, product_type: Optional[str] = None) -> List[Dict]:
        """Search by brand with Tier 2 field support"""
        query = brand
        if product_type:
            query += f" {product_type}"

        results = self.search(query)

        # Add Tier 2 fields
        for result in results:
            result['tier2_fields'] = {
                'brand': brand,
                'model': self._extract_model(result['name'], brand),
                'category': 'audio'
            }

        return results

    def _extract_model(self, text: str, brand: str) -> str:
        """Extract model from product name"""
        # Remove brand from text
        text = text.replace(brand, '').strip()
        # Take first few words as model
        words = text.split()[:3]
        return ' '.join(words)

class PriceChartingScraper(BaseScraper):
    """PriceCharting scraper for games/collectibles"""

    def __init__(self, retailer_id: int, base_url: str = "https://www.pricecharting.com"):
        super().__init__(retailer_id, base_url)

    def search(self, query: str, **kwargs) -> List[Dict]:
        """Search PriceCharting"""
        search_url = f"{self.base_url}/search?q={quote_plus(query)}"
        soup = self.fetch(search_url)

        if not soup:
            return []

        results = []
        items = soup.select('.search-result')

        for item in items:
            try:
                title = item.select_one('.title, h3')
                price = item.select_one('.price')
                console = item.select_one('.console, .category')

                if title:
                    results.append({
                        'name': title.get_text(strip=True),
                        'price': self.parse_price(price.get_text()) if price else 0,
                        'set_name': console.get_text(strip=True) if console else None,
                        'category': kwargs.get('category', 'collectibles')
                    })
            except Exception as e:
                print(f"Error: {e}")

        return results

    def get_product_details(self, product_url: str) -> Dict:
        """Get details"""
        soup = self.fetch(product_url)
        if not soup:
            return {}

        return {
            'name': soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else '',
            'set_name': soup.select_one('.console').get_text(strip=True) if soup.select_one('.console') else '',
            'category': 'collectibles'
        }

    def parse_price(self, price_text: str) -> float:
        """Parse price"""
        import re
        match = re.search(r'\$([\d,]+(?:\.\d{2})?)', price_text)
        if match:
            return float(match.group(1).replace(',', ''))
        return 0.0
