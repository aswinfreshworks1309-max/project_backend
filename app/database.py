 
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
