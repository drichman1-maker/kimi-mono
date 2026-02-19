# API Documentation

## Base URL
```
Local: http://localhost:8000/api/v1
Production: https://your-api.render.com/api/v1
```

## Authentication
Currently open API. Authentication can be added via FastAPI dependencies.

## Endpoints

### Products

#### List Products
```http
GET /products/?skip=0&limit=100&category=mac&search=MacBook
```

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Items per page (max 100)
- `category` (string): Filter by category
- `search` (string): Search in name/description

**Response:**
```json
[
  {
    "id": 1,
    "name": "MacBook Pro 14 M3",
    "category": "mac",
    "description": "Latest MacBook Pro",
    "model_identifier": "Mac15,3",
    "release_year": 2023,
    "specs": {"cpu": "M3", "ram": "16GB", "storage": "512GB"},
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

#### Advanced Search
```http
POST /products/search
```

**Request Body:**
```json
{
  "query": "MacBook Pro",
  "category": "mac",
  "min_price": 1000,
  "max_price": 3000,
  "brand": "Apple",
  "release_year": 2023
}
```

**Response:** Products with prices and stats

#### Create Product
```http
POST /products/
```

**Request Body:**
```json
{
  "name": "MacBook Pro 14 M3",
  "category": "mac",
  "description": "Space Black, M3 Pro",
  "model_identifier": "Mac15,3",
  "release_year": 2023,
  "specs": {
    "cpu": "M3 Pro",
    "ram": "18GB",
    "storage": "512GB SSD"
  }
}
```

#### Get Product with Prices
```http
GET /products/{product_id}
```

**Response:**
```json
{
  "id": 1,
  "name": "MacBook Pro 14 M3",
  "category": "mac",
  "prices": [
    {
      "id": 1,
      "price": 1999.00,
      "retailer_name": "eBay",
      "condition": "new",
      "listing_url": "https://..."
    }
  ],
  "price_stats": {
    "count": 5,
    "avg": 2100.00,
    "min": 1999.00,
    "max": 2299.00
  }
}
```

#### Price Comparison
```http
GET /products/{product_id}/comparison
```

**Response:**
```json
{
  "product": { ... },
  "prices": [ ... ],
  "best_price": { ... },
  "avg_price": 2100.00,
  "price_range": {"min": 1999.00, "max": 2299.00}
}
```

#### Add Price
```http
POST /products/{product_id}/prices
```

**Request Body:**
```json
{
  "retailer_id": 1,
  "price": 1999.00,
  "condition": "new",
  "listing_url": "https://ebay.com/...",
  "listing_title": "MacBook Pro 14"
}
```

### Categories

#### List Categories
```http
GET /products/categories
```

**Response:**
```json
[
  {
    "id": "mac",
    "name": "Apple/Mac Products",
    "tier2_fields": ["model_identifier", "release_year", "specs"]
  },
  {
    "id": "pokemon",
    "name": "Pokemon Cards",
    "tier2_fields": ["set_name", "card_number", "rarity", "condition"]
  }
]
```

### Price Alerts

#### Create Alert
```http
POST /alerts/
```

**Request Body:**
```json
{
  "product_id": 1,
  "target_price": 1800.00,
  "condition": "below",
  "email": "user@example.com"
}
```

#### List Alerts
```http
GET /alerts/?product_id=1&is_active=true
```

#### Check Alerts (Manual)
```http
POST /alerts/check
```

**Response:**
```json
{
  "checked": true,
  "triggered": [1, 2, 3]
}
```

### Retailers

#### List Retailers
```http
GET /retailers/?scraper_type=ebay
```

#### Create Retailer
```http
POST /retailers/
```

**Request Body:**
```json
{
  "name": "eBay",
  "base_url": "https://www.ebay.com",
  "scraper_type": "ebay",
  "config": {
    "api_key": "optional",
    "rate_limit": 1.0
  }
}
```

## Error Responses

```json
{
  "detail": "Product not found"
}
```

**Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `422` - Validation Error
- `500` - Server Error

## Rate Limiting

Default rate limits:
- Scrapers: 1 request per 2-5 seconds
- API: No limit (add via middleware if needed)

## Webhooks

Alert webhooks receive POST requests:

```json
{
  "product_id": 1,
  "product_name": "MacBook Pro",
  "current_price": 1799.00,
  "target_price": 1800.00,
  "condition": "below"
}
```
