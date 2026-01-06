 
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# --- AUTO-FIX LOGIC ---
if DATABASE_URL:
    # 1. Fix host if it's the old one
    if "db.unyrqhgrzialltsdubow.supabase.co" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("db.unyrqhgrzialltsdubow.supabase.co", "aws-1-ap-south-1.pooler.supabase.com").replace(":5432", ":6543")
    
    # 2. Fix password typo if it exists in the current URL (Missing 'd')
    if "AcademyRootPasswor" in DATABASE_URL and "AcademyRootPassword" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("AcademyRootPasswor", "AcademyRootPassword")
# ----------------------

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
