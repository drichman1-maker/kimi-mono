# Deployment Guide

## Render.com Deployment

### 1. Prepare Repository

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/price-aggregator-api.git
git push -u origin main
```

### 2. Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "PostgreSQL"
3. Name: `price-aggregator-db`
4. Plan: Free (or paid for production)
5. Create Database
6. Copy the "Internal Database URL"

### 3. Deploy Web Service

**Option A: Blueprint Deploy (Recommended)**

1. Push `render.yaml` to your repo
2. In Render dashboard, click "Blueprints"
3. Connect your GitHub repo
4. Render will auto-create services from `render.yaml`

**Option B: Manual Deploy**

1. Click "New" → "Web Service"
2. Connect your GitHub repo
3. Configure:
   - **Name**: `price-aggregator-api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `DATABASE_URL`: (from step 2)
   - `PYTHON_VERSION`: 3.11.0
5. Create Web Service

### 4. Run Migrations

In Render dashboard:
1. Go to your web service
2. Click "Shell" tab
3. Run:
```bash
alembic upgrade head
```

### 5. Verify Deployment

```bash
curl https://your-service.onrender.com/health
```

Should return: `{"status": "healthy"}`

## Docker Deployment

### Local with Docker Compose

```bash
docker-compose up -d
```

Services:
- API: http://localhost:8000
- PostgreSQL: localhost:5432

### Production Docker

```bash
# Build
docker build -t price-aggregator-api .

# Run
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  price-aggregator-api
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `SMTP_SERVER` | No | Email server (default: smtp.gmail.com) |
| `SMTP_PORT` | No | Email port (default: 587) |
| `SMTP_USERNAME` | No | Email username |
| `SMTP_PASSWORD` | No | Email password |
| `FROM_EMAIL` | No | From address (default: alerts@priceaggregator.com) |

## Health Checks

- `/` - API info
- `/health` - Health status
- `/docs` - Swagger UI

## Troubleshooting

### Database Connection Issues

```bash
# Test connection
psql $DATABASE_URL -c "SELECT 1;"
```

### Migration Errors

```bash
# Reset migrations (careful - data loss)
alembic downgrade base
alembic upgrade head
```

### Scraper Not Running

Check logs in Render dashboard:
- Go to web service → Logs
- Look for scraper initialization messages

## Scaling

### Render
- Upgrade to paid plan
- Increase instance count
- Add background workers

### Database
- Upgrade PostgreSQL plan
- Add connection pooling
- Enable read replicas

## Security Checklist

- [ ] Change default database passwords
- [ ] Enable HTTPS only
- [ ] Add API authentication
- [ ] Restrict CORS origins
- [ ] Add rate limiting
- [ ] Enable database SSL
- [ ] Use secrets manager for credentials
