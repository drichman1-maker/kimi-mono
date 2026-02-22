# Price Aggregator API

A comprehensive FastAPI-based price aggregation service with Tier 1-2 field support for multi-category products including Mac computers, Pokemon cards, audio equipment, and collectibles.

## Features

- **Multi-Category Support**: Mac, Pokemon, Audio, Electronics, Collectibles
- **Tier 1-2 Field Architecture**: Common fields + category-specific attributes
- **Multi-Retailer Scraping**: eBay, Reverb, PriceCharting, TCGPlayer
- **Price Alerts**: Telegram notifications for price drops & restocks
- **Price History**: Track price changes over time
- **RESTful API**: Full CRUD operations with filtering
- **Cron Integration**: GitHub Actions or cron-job.org for scheduled checks

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
- `POST /api/v1/alerts/check` - Trigger alert check (manual)
- `POST /api/v1/alerts/trigger-check` - Webhook for cron jobs
  - Query params: `check_type` = `price_drops`, `restocks`, or `summary`
  - Header: `X-Cron-Secret` (optional, for authentication)

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

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Telegram Alerts (required for notifications)
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Cron Security (optional)
CRON_SECRET=your-secret-key-for-cron-webhooks

# SMTP (optional, for email alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=alerts@priceaggregator.com
```

## Price Alert Setup

### 1. Get Telegram Credentials

1. Message [@BotFather](https://t.me/BotFather) on Telegram to create a bot (or use existing @Markydoesitbot)
2. Copy the bot token
3. Message [@userinfobot](https://t.me/userinfobot) to get your chat ID
4. Add to your `.env` file

### 2. Test Telegram Integration

```bash
python test_telegram.py
```

### 3. Set Up Cron Job (Choose One)

#### Option A: GitHub Actions (Free)

1. Fork/push repo to GitHub
2. Go to **Settings → Secrets and variables → Actions**
3. Add secrets:
   - `API_URL`: Your deployed API URL (e.g., `https://mactrackr-api.onrender.com`)
   - `CRON_SECRET`: Same as your `CRON_SECRET` env var
4. Workflow runs automatically every hour during business hours

#### Option B: cron-job.org (Free, No GitHub needed)

1. Sign up at [cron-job.org](https://cron-job.org)
2. Create new cron job:
   - **URL**: `https://your-api.com/api/v1/alerts/trigger-check?check_type=price_drops`
   - **Method**: POST
   - **Headers**: `X-Cron-Secret: your-secret`
   - **Schedule**: Every 30 minutes

#### Option C: Self-hosted (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add line (runs every 30 minutes during business hours)
*/30 8-22 * * * curl -X POST "https://your-api.com/api/v1/alerts/trigger-check" -H "X-Cron-Secret: your-secret"
```

### Alert Types

The cron endpoint supports three check types:

- **`price_drops`**: Checks all active alerts, sends Telegram notifications for price drops ≥5% or below target price
- **`restocks`**: Notifies when out-of-stock items come back in stock
- **`summary`**: Sends daily summary of tracked products and price changes

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
│   │   ├── alerts.py        # Alert API with Telegram
│   │   └── retailers.py     # Retailer API
│   └── services/
│       ├── scraper_service.py
│       └── telegram_service.py  # Telegram notifications
├── scrapers/
│   ├── base.py              # Base scraper class
│   ├── tier1_2_scrapers.py  # eBay, Reverb, PriceCharting
│   ├── mac_scraper.py       # Apple-specific
│   ├── pokemon_scraper.py   # Pokemon-specific
│   └── runner.py            # Scheduler
├── .github/workflows/
│   └── price-alerts.yml     # GitHub Actions cron job
├── tests/
├── alembic/                 # DB migrations
├── README.md
├── API.md                   # Detailed API docs
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── render.yaml              # Render.com config
├── .env.example             # Environment template
└── test_telegram.py         # Test Telegram integration
```

## Testing

```bash
pytest tests/
```

## License

MIT
