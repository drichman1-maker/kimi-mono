"""
Price Aggregator API - Main Application
FastAPI entry point with Tier 1-2 field support
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import products, alerts, retailers

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("🚀 Price Aggregator API starting...")
    try:
        # Test database connection without creating tables
        from app.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connected")
    except Exception as e:
        print(f"⚠️ Database not ready: {e}")
    yield
    print("🛑 Price Aggregator API shutting down...")

app = FastAPI(
    title="Price Aggregator API",
    description="Multi-category price tracking with Tier 1-2 field support",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])
app.include_router(retailers.router, prefix="/api/v1", tags=["retailers"])

@app.get("/")
async def root():
    return {
        "message": "Price Aggregator API",
        "version": "2.0.0",
        "docs": "/docs",
        "features": ["Tier 1-2 fields", "Multi-category", "Price alerts"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "price-aggregator-api"}
