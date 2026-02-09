import sys
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

print("=" * 60)
print("RENDER DATABASE CONNECTION TEST")
print("=" * 60)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("✗ No DATABASE_URL found in .env")
    sys.exit(1)

# Check for internal vs external URL
if "-a.virginia-postgres.render.com" in DATABASE_URL:
    print("! WARNING: You appear to be using an INTERNAL Render URL.")
    print("! These only work when your code is running ON Render.")
    print("! Please use the EXTERNAL Connection String from your dashboard.")

# Add sslmode=require if not present
if "sslmode=" not in DATABASE_URL and "render.com" in DATABASE_URL:
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"

try:
    print("\nAttempting to connect...")
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()
        print(f"✓ SUCCESS! Connected to: {version[0]}")
        
    print("\nAttempting to import app modules...")
    from app.database import SessionLocal
    from app import models
    print("✓ app modules imported successfully")
except Exception as e:
    print(f"\n✗ CONNECTION FAILED: {e}")
    print("\nPossible fixes:")
    print("1. Use the 'External Connection String' from Render.")
    print("2. Ensure your IP is allowed in Render's Access Control (if enabled).")
    print("3. Check your internet connection.")
    sys.exit(1)

