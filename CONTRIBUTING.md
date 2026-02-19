# Contributing to Price Aggregator API

## Development Setup

```bash
# Clone repo
git clone https://github.com/yourusername/price-aggregator-api.git
cd price-aggregator-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks (optional)
pre-commit install
```

## Project Structure

```
price-aggregator-api/
├── app/                    # Main application
│   ├── main.py            # FastAPI entry point
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # DB connection
│   ├── routers/           # API endpoints
│   └── services/          # Business logic
├── scrapers/              # Web scrapers
├── tests/                 # Test suite
├── alembic/               # Database migrations
└── docs/                  # Documentation
```

## Adding a New Scraper

1. Create scraper class in `scrapers/`:
```python
from scrapers.base import BaseScraper

class NewScraper(BaseScraper):
    def search(self, query: str, **kwargs):
        # Implementation
        pass

    def get_product_details(self, product_url: str):
        # Implementation
        pass

    def parse_price(self, price_text: str) -> float:
        # Implementation
        pass
```

2. Register in `scrapers/runner.py`
3. Add tests in `tests/test_scrapers.py`
4. Update documentation

## Adding a New Category

1. Update `Category` enum in `app/schemas.py`
2. Add Tier 2 fields to `app/models.py`
3. Update search filters in `app/routers/products.py`
4. Add category info to `get_categories()` endpoint
5. Create/update scraper
6. Update documentation

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov=scrapers

# Run specific test
pytest tests/test_products.py::test_create_product -v
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit pull request

## Code Review Checklist

- [ ] Tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Error handling implemented
- [ ] Rate limiting considered (for scrapers)
