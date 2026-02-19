"""
Price Aggregator API - Main Application
FastAPI entry point with Tier 1-2 field support
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import products, alerts, retailers

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events - non-blocking startup"""
    print("🚀 Price Aggregator API starting...")
    print("✅ API ready (database connects lazily)")
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
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check - always returns ok"""
    return {"status": "healthy", "service": "price-aggregator-api"}
