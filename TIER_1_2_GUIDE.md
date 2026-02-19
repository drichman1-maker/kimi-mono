# Tier 1-2 Field System Guide

## Overview

The Price Aggregator API uses a two-tier field system to handle diverse product categories efficiently.

- **Tier 1**: Common fields shared by ALL products
- **Tier 2**: Category-specific fields stored in dedicated columns or JSON

## Tier 1 Fields (Universal)

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String(500) | Product name |
| `category` | String(50) | Product category |
| `description` | Text | Full description |
| `image_url` | String(500) | Primary image URL |
| `source_url` | String(500) | Original listing URL |
| `is_active` | Boolean | Active status |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

## Tier 2 Fields by Category

### Mac Products (`category = "mac"`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `model_identifier` | String(100) | Apple model ID | "Mac15,3" |
| `release_year` | Integer | Release year | 2023 |
| `specs` | JSON | Technical specs | `{"cpu": "M3", "ram": "16GB"}` |

**Spec JSON Structure:**
```json
{
  "cpu": "Apple M3 Pro",
  "ram": "18GB",
  "storage": "512GB SSD",
  "screen_size": "14.2 inch",
  "gpu": "14-core GPU",
  "color": "Space Black"
}
```

### Pokemon Cards (`category = "pokemon"`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `set_name` | String(100) | Card set | "Scarlet & Violet" |
| `card_number` | String(20) | Set number | "123/198" |
| `rarity` | String(50) | Card rarity | "Holo Rare" |
| `condition` | String(20) | Card condition | "NM" |

**Condition Values:**
- `NM` - Near Mint
- `LP` - Light Play
- `MP` - Moderate Play
- `HP` - Heavy Play
- `DMG` - Damaged

### Audio/Music Gear (`category = "audio"`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `brand` | String(100) | Manufacturer | "Fender" |
| `model` | String(100) | Model name | "Stratocaster" |

### Electronics (`category = "electronics"`)

| Field | Type | Description |
|-------|------|-------------|
| `brand` | String(100) | Manufacturer |
| `model` | String(100) | Model number |
| `specs` | JSON | Technical specifications |

### Collectibles (`category = "collectibles"`)

| Field | Type | Description |
|-------|------|-------------|
| `condition` | String(20) | Item condition |
| `rarity` | String(50) | Rarity level |

## Flexible Attributes

All products also have an `attributes` JSON field for custom data:

```json
{
  "custom_field_1": "value",
  "tags": ["vintage", "limited"],
  "metadata": { ... }
}
```

## API Usage Examples

### Creating a Mac Product

```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro 14-inch M3",
    "category": "mac",
    "description": "Latest MacBook Pro with M3 chip",
    "model_identifier": "Mac15,3",
    "release_year": 2023,
    "specs": {
      "cpu": "Apple M3",
      "ram": "16GB",
      "storage": "512GB",
      "color": "Space Gray"
    }
  }'
```

### Creating a Pokemon Card

```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Charizard EX",
    "category": "pokemon",
    "description": "Rare Charizard card",
    "set_name": "Scarlet & Violet",
    "card_number": "125/198",
    "rarity": "Ultra Rare",
    "condition": "NM"
  }'
```

### Searching with Tier 2 Filters

```bash
curl -X POST "http://localhost:8000/api/v1/products/search" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "mac",
    "brand": "Apple",
    "release_year": 2023,
    "min_price": 1500,
    "max_price": 2500
  }'
```

## Database Schema

```sql
-- Tier 1 fields (columns)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(500),
    category VARCHAR(50),
    description TEXT,
    image_url VARCHAR(500),
    source_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Tier 2: Mac
    model_identifier VARCHAR(100),
    release_year INTEGER,
    specs JSONB DEFAULT '{}',

    -- Tier 2: Pokemon
    set_name VARCHAR(100),
    card_number VARCHAR(20),
    rarity VARCHAR(50),
    condition VARCHAR(20),

    -- Tier 2: Audio
    brand VARCHAR(100),
    model VARCHAR(100),

    -- Flexible
    attributes JSONB DEFAULT '{}'
);
```

## Best Practices

1. **Always set `category`** - Required for Tier 2 field validation
2. **Use appropriate Tier 2 fields** - Don't put Mac specs in Pokemon cards
3. **Keep `specs` structured** - Use consistent keys within categories
4. **Use `attributes` sparingly** - For truly custom data only
5. **Index category field** - Always filter by category first for performance

## Migration Guide

Adding a new category:

1. Add Tier 2 columns to `models.py`
2. Update `schemas.py` with validation
3. Add category to `Category` enum
4. Update search filters in `products.py`
5. Create scraper in `scrapers/`
6. Update documentation
