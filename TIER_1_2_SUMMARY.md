# Tier 1-2 Quick Reference

## Field Matrix

| Category | Tier 2 Fields | Use Case |
|----------|---------------|----------|
| **mac** | `model_identifier`, `release_year`, `specs` | Apple computers |
| **pokemon** | `set_name`, `card_number`, `rarity`, `condition` | Trading cards |
| **audio** | `brand`, `model` | Music gear |
| **electronics** | `brand`, `model`, `specs` | General electronics |
| **collectibles** | `condition`, `rarity` | Collectible items |
| **other** | `attributes` (flexible) | Uncategorized |

## API Quick Reference

### Create Product
```http
POST /api/v1/products/
Content-Type: application/json

{
  "name": "Product Name",
  "category": "mac|pokemon|audio|electronics|collectibles|other",
  "description": "...",

  // Mac fields
  "model_identifier": "Mac15,3",
  "release_year": 2023,
  "specs": {"cpu": "M3", "ram": "16GB"},

  // Pokemon fields  
  "set_name": "Scarlet & Violet",
  "card_number": "123/198",
  "rarity": "Holo Rare",
  "condition": "NM",

  // Audio fields
  "brand": "Fender",
  "model": "Stratocaster",

  // Generic
  "attributes": {"custom": "value"}
}
```

### Search with Filters
```http
POST /api/v1/products/search
Content-Type: application/json

{
  "query": "search text",
  "category": "mac",
  "min_price": 100,
  "max_price": 1000,

  // Mac filters
  "brand": "Apple",
  "release_year": 2023,

  // Pokemon filters
  "set_name": "Base Set",
  "rarity": "Rare"
}
```

## Category Endpoints

```http
GET /api/v1/products/categories
```

Returns available categories with their Tier 2 fields.

## Scrapers by Category

| Category | Scrapers |
|----------|----------|
| mac | eBay, MacSales, EveryMac |
| pokemon | eBay, PriceCharting, TCGPlayer |
| audio | eBay, Reverb |
| electronics | eBay |
| collectibles | eBay, PriceCharting |

## Common Patterns

### Mac Product
```json
{
  "name": "MacBook Pro 14 M3",
  "category": "mac",
  "model_identifier": "Mac15,3",
  "release_year": 2023,
  "specs": {
    "cpu": "Apple M3 Pro",
    "ram": "18GB",
    "storage": "512GB SSD",
    "color": "Space Black"
  }
}
```

### Pokemon Card
```json
{
  "name": "Charizard EX",
  "category": "pokemon",
  "set_name": "Scarlet & Violet",
  "card_number": "125/198",
  "rarity": "Ultra Rare",
  "condition": "NM"
}
```

### Audio Gear
```json
{
  "name": "Fender Stratocaster",
  "category": "audio",
  "brand": "Fender",
  "model": "American Professional II"
}
```

## Validation Rules

- `category` is **required**
- `name` must be 1-500 characters
- `release_year` must be 2000-2030
- `condition` must be: new, used, refurbished, NM, LP, MP, HP, DMG
- `rarity` is free text but recommended values provided

## Database Indexes

```sql
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_model_id ON products(model_identifier);
CREATE INDEX idx_products_set_name ON products(set_name);
CREATE INDEX idx_products_brand ON products(brand);
```
