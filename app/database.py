"""
Database configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Debug: log what we got (hide password)
if DATABASE_URL:
    safe_url = DATABASE_URL.replace(DATABASE_URL.split(":")[2].split("@")[0], "***") if "://" in DATABASE_URL else "***"
    print(f"🔌 DATABASE_URL found: {safe_url}")
else:
    print("⚠️ DATABASE_URL not set! Checking Railway variables...")
    # Try alternative env vars Railway might use
    for var in ["RAILWAY_DATABASE_URL", "PGDATABASE", "DATABASE_URI"]:
        val = os.getenv(var)
        if val:
            print(f"✅ Found {var}")
            DATABASE_URL = val
            break

# Railway uses postgres://, SQLAlchemy needs postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/price_aggregator"
    print("⚠️ Using fallback localhost database")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
