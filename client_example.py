"""
MacTrackr Integration Example
Shows how to use the Price Aggregator API from a client application
"""

import requests
import json
from typing import List, Dict, Optional

class PriceAggregatorClient:
    """Client for Price Aggregator API"""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()

    def health_check(self) -> bool:
        """Check API health"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False

    # Products
    def list_products(self, category: str = None, search: str = None) -> List[Dict]:
        """List products with optional filters"""
        params = {}
        if category:
            params["category"] = category
        if search:
            params["search"] = search

        response = self.session.get(f"{self.base_url}/products/", params=params)
        response.raise_for_status()
        return response.json()

    def search_products(self, **filters) -> List[Dict]:
        """Advanced search with Tier 1-2 filters"""
        response = self.session.post(
            f"{self.base_url}/products/search",
            json=filters
        )
        response.raise_for_status()
        return response.json()

    def get_product(self, product_id: int) -> Dict:
        """Get product with prices"""
        response = self.session.get(f"{self.base_url}/products/{product_id}")
        response.raise_for_status()
        return response.json()

    def create_product(self, product_data: Dict) -> Dict:
        """Create a new product"""
        response = self.session.post(
            f"{self.base_url}/products/",
            json=product_data
        )
        response.raise_for_status()
        return response.json()

    def compare_prices(self, product_id: int) -> Dict:
        """Get price comparison across retailers"""
        response = self.session.get(
            f"{self.base_url}/products/{product_id}/comparison"
        )
        response.raise_for_status()
        return response.json()

    # Categories
    def get_categories(self) -> List[Dict]:
        """Get available categories with Tier 2 fields"""
        response = self.session.get(f"{self.base_url}/products/categories")
        response.raise_for_status()
        return response.json()

    # Alerts
    def create_alert(self, product_id: int, target_price: float, 
                     condition: str = "below", email: str = None) -> Dict:
        """Create price alert"""
        data = {
            "product_id": product_id,
            "target_price": target_price,
            "condition": condition,
            "email": email
        }
        response = self.session.post(f"{self.base_url}/alerts/", json=data)
        response.raise_for_status()
        return response.json()

    def list_alerts(self, product_id: int = None) -> List[Dict]:
        """List price alerts"""
        params = {}
        if product_id:
            params["product_id"] = product_id
        response = self.session.get(f"{self.base_url}/alerts/", params=params)
        response.raise_for_status()
        return response.json()

# MacTrackr Integration Example
class MacTrackrIntegration:
    """Example integration for Mac product tracking"""

    def __init__(self, api_url: str = "http://localhost:8000/api/v1"):
        self.client = PriceAggregatorClient(api_url)

    def find_mac_products(self, model: str = None, year: int = None) -> List[Dict]:
        """Find Mac products with Tier 2 filters"""
        filters = {
            "category": "mac",
            "query": model or "MacBook"
        }
        if year:
            filters["release_year"] = year

        return self.client.search_products(**filters)

    def add_mac_product(self, name: str, model_id: str, year: int, specs: Dict) -> Dict:
        """Add a Mac product with full Tier 2 fields"""
        product = {
            "name": name,
            "category": "mac",
            "model_identifier": model_id,
            "release_year": year,
            "specs": specs
        }
        return self.client.create_product(product)

    def get_best_price(self, product_id: int) -> Optional[Dict]:
        """Get best price for a Mac product"""
        comparison = self.client.compare_prices(product_id)
        return comparison.get("best_price")

    def setup_price_alert(self, product_id: int, target_price: float, email: str):
        """Set up price alert for Mac product"""
        return self.client.create_alert(
            product_id=product_id,
            target_price=target_price,
            condition="below",
            email=email
        )

# Example usage
def main():
    """Example usage of the API client"""

    # Initialize client
    client = PriceAggregatorClient("http://localhost:8000/api/v1")

    # Check health
    if not client.health_check():
        print("❌ API is not available")
        return
    print("✅ API is healthy")

    # Get categories
    print("\n📋 Available Categories:")
    categories = client.get_categories()
    for cat in categories:
        print(f"  - {cat['name']}: {', '.join(cat['tier2_fields'])}")

    # Search for Mac products
    print("\n🔍 Searching for Mac products...")
    mac_products = client.search_products(
        category="mac",
        query="MacBook Pro",
        release_year=2023
    )

    for product in mac_products[:3]:
        print(f"\n  💻 {product['name']}")
        print(f"     Model: {product.get('model_identifier', 'N/A')}")
        print(f"     Year: {product.get('release_year', 'N/A')}")
        if product.get('price_stats'):
            stats = product['price_stats']
            print(f"     Prices: ${stats['min']} - ${stats['max']} (avg: ${stats['avg']})")

    # MacTrackr integration example
    print("\n🚀 MacTrackr Integration Example:")
    mactrackr = MacTrackrIntegration()

    # Find 2023 MacBooks
    macs_2023 = mactrackr.find_mac_products(year=2023)
    print(f"Found {len(macs_2023)} Mac products from 2023")

    # If products exist, show comparison
    if macs_2023:
        product = macs_2023[0]
        print(f"\nComparing prices for: {product['name']}")

        comparison = client.compare_prices(product['id'])
        print(f"Best price: ${comparison['best_price']['price']} at {comparison['best_price']['retailer_name']}")
        print(f"Average price: ${comparison['avg_price']}")
        print(f"Savings: ${comparison['avg_price'] - comparison['best_price']['price']:.2f}")

if __name__ == "__main__":
    main()
