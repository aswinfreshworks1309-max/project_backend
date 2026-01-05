 
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# --- AUTO-FIX LOGIC ---
# If the backend is still using the old direct Supabase host, we force it to use the new Pooler URL
# locally and on Vercel to prevent connection failures.
if DATABASE_URL and "db.unyrqhgrzialltsdubow.supabase.co" in DATABASE_URL:
    # Reconstructing the correct Pooler URL using the known password and project ref
    DATABASE_URL = "postgresql://postgres.unyrqhgrzialltsdubow:AcademyRootPassword@aws-1-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"
# ----------------------

if not DATABASE_URL:
    # Do not crash on import, allows checking root endpoint
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
