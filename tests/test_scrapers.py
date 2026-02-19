"""
Tests for scrapers
"""

import pytest
from scrapers.base import GenericScraper
from scrapers.tier1_2_scrapers import eBayScraper, ReverbScraper

def test_base_scraper_parse_price():
    """Test price parsing"""
    scraper = GenericScraper(1, "https://example.com")

    # Test various price formats
    assert scraper.parse_price("$1,234.56") == 1234.56
    assert scraper.parse_price("$999") == 999.0
    assert scraper.parse_price("Price: $1,299.00") == 1299.0
    assert scraper.parse_price("Invalid") == 0.0

def test_ebay_scraper_init():
    """Test eBay scraper initialization"""
    scraper = eBayScraper(1)
    assert scraper.retailer_id == 1
    assert scraper.base_url == "https://www.ebay.com"

def test_reverb_scraper_init():
    """Test Reverb scraper initialization"""
    scraper = ReverbScraper(2)
    assert scraper.retailer_id == 2
    assert scraper.base_url == "https://reverb.com"

def test_ebay_parse_price():
    """Test eBay price parsing"""
    scraper = eBayScraper(1)

    assert scraper.parse_price("$1,234.56") == 1234.56
    assert scraper.parse_price("$100.00 to $150.00") == 100.00
    assert scraper.parse_price("Current bid: $50.00") == 50.0
