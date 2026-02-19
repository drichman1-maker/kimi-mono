"""
Tests for product endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_products():
    """Test listing products"""
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_products_with_category():
    """Test filtering by category"""
    response = client.get("/api/v1/products/?category=mac")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_categories():
    """Test getting categories"""
    response = client.get("/api/v1/products/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "tier2_fields" in data[0]

def test_create_product():
    """Test creating a product"""
    product_data = {
        "name": "Test MacBook",
        "category": "mac",
        "description": "Test description",
        "model_identifier": "MacTest1",
        "release_year": 2023,
        "specs": {"cpu": "Test", "ram": "16GB"}
    }
    response = client.post("/api/v1/products/", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["category"] == product_data["category"]
    return data["id"]

def test_search_products():
    """Test searching products"""
    search_data = {
        "query": "MacBook",
        "category": "mac",
        "min_price": 1000
    }
    response = client.post("/api/v1/products/search", json=search_data)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_nonexistent_product():
    """Test getting a product that doesn't exist"""
    response = client.get("/api/v1/products/99999")
    assert response.status_code == 404
