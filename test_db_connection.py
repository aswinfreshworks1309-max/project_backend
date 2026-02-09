import sys
import os
from dotenv import load_dotenv

print("Testing database connection...")
print("=" * 60)

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Mask the password for security
    masked_url = DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL
    print(f"✓ DATABASE_URL found: ...@{masked_url}")
else:
    print("✗ DATABASE_URL not found in .env file")
    sys.exit(1)

try:
    from app.database import SessionLocal, engine, Base
    print("✓ Imported database modules")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

try:
    # Test connection
    print("\nTesting database connection...")
    db = SessionLocal()
    print("✓ Database connection successful")
    
    # Import models
    from app import models
    print("✓ Models imported")
    
    # Create tables
    print("\nCreating/verifying tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created/verified")
    
    # Check if any buses exist
    bus_count = db.query(models.Bus).count()
    schedule_count = db.query(models.Schedule).count()
    
    print(f"\nCurrent database status:")
    print(f"  - Buses: {bus_count}")
    print(f"  - Schedules: {schedule_count}")
    
    db.close()
    print("\n✓ Database test completed successfully!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ Database error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
