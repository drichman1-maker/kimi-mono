# Price Aggregator API

A comprehensive FastAPI-based price aggregation service with Tier 1-2 field support for multi-category products including Mac computers, Pokemon cards, audio equipment, and collectibles.

## Features

- **Multi-Category Support**: Mac, Pokemon, Audio, Electronics, Collectibles
- **Tier 1-2 Field Architecture**: Common fields + category-specific attributes
- **Multi-Retailer Scraping**: eBay, Reverb, PriceCharting, TCGPlayer
- **Price Alerts**: Email and webhook notifications
- **Price History**: Track price changes over time
- **RESTful API**: Full CRUD operations with filtering

## Quick Start

### Local Development

```bash
# Clone and setup
cd price-aggregator-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup database
# Update DATABASE_URL in .env or use default PostgreSQL
# Default: postgresql://postgres:postgres@localhost:5432/price_aggregator

# Run migrations
alembic upgrade head

# Seed data (optional)
python seed_data.py

# Start server
uvicorn app.main:app --reload
```

### Docker

```bash
docker-compose up -d
```

### Deploy to Render

1. Push to GitHub
2. Connect repo to Render
3. Add PostgreSQL database
4. Deploy using `render.yaml` blueprint

## API Endpoints

### Products
- `GET /api/v1/products/` - List products
- `POST /api/v1/products/search` - Advanced search with filters
- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/{id}` - Get product details
- `GET /api/v1/products/{id}/comparison` - Price comparison
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

### Categories
- `GET /api/v1/products/categories` - List categories with Tier 2 fields

### Alerts
- `GET /api/v1/alerts/` - List alerts
- `POST /api/v1/alerts/` - Create alert
- `POST /api/v1/alerts/check` - Trigger alert check

### Retailers
- `GET /api/v1/retailers/` - List retailers
- `POST /api/v1/retailers/` - Add retailer

## Tier 1-2 Field System

### Tier 1 (Common Fields)
All products have:
- `name`, `category`, `description`, `image_url`
- `source_url`, `is_active`, `created_at`, `updated_at`

### Tier 2 (Category-Specific)

**Mac Products:**
- `model_identifier` (e.g., "Mac15,3")
- `release_year`
- `specs` (JSON: CPU, RAM, Storage, etc.)

**Pokemon Cards:**
- `set_name`, `card_number`, `rarity`, `condition`

**Audio/Music:**
- `brand`, `model`

## Scrapers

### Supported Retailers

| Retailer | Type | Categories |
|----------|------|------------|
| eBay | Marketplace | All |
| Reverb | Audio/Music | Audio |
| PriceCharting | Collectibles | Pokemon, Games |
| TCGPlayer | Trading Cards | Pokemon |

### Running Scrapers

```python
# Manual run
python -c "from scrapers.runner import run_scraper_now; print(run_scraper_now(1, 'MacBook Pro'))"

# Scheduled (automatic)
# Scrapers run every 60 minutes by default
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=alerts@priceaggregator.com
```

## Project Structure

```
price-aggregator-api/
├── app/
│   ├── main.py              # FastAPI entry
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # DB connection
│   ├── routers/
│   │   ├── products.py      # Product API
│   │   ├── alerts.py        # Alert API
│   │   └── retailers.py     # Retailer API
│   └── services/
│       └── scraper_service.py
├── scrapers/
│   ├── base.py              # Base scraper class
│   ├── tier1_2_scrapers.py  # eBay, Reverb, PriceCharting
│   ├── mac_scraper.py       # Apple-specific
│   ├── pokemon_scraper.py   # Pokemon-specific
│   └── runner.py            # Scheduler
├── tests/
├── alembic/                 # DB migrations
├── README.md
├── API.md                   # Detailed API docs
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── render.yaml              # Render.com config
```

## Testing

```bash
pytest tests/
```

## License

MIT
