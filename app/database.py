 
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# --- AUTO-FIX LOGIC ---

if not DATABASE_URL:
    engine = None
    SessionLocal = None
else:
    # Ensure synchronous driver for SQLAlchemy and add SSL requirement for Supabase/Cloud
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    # Add sslmode=require if not present for cloud databases
    if "supabase.co" in DATABASE_URL or "neon.tech" in DATABASE_URL:
        if "sslmode" not in DATABASE_URL:
            separator = "&" if "?" in DATABASE_URL else "?"
            DATABASE_URL += f"{separator}sslmode=require"

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency
def get_db():
    if SessionLocal is None:
        raise Exception("Database not configured. DATABASE_URL env var is missing.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
