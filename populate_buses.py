
import os
import random
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 1. Load your local settings
load_dotenv()
DATABASE_URL = "postgresql://postgres:AcademyRootPassword@localhost:5432/database_bus"

print("=" * 60)
print("DIRECT POSTGRESQL POPULATION - LOCAL pgAdmin")
print("=" * 60)

# 2. Setup Database
try:
    engine = create_engine(DATABASE_URL)
    # Test connection immediately
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✓ SUCCESSFULLY CONNECTED TO LOCAL POSTGRESQL")
except Exception as e:
    print(f"✗ CONNECTION FAILED: {e}")
    print("\nHELP: Is pgAdmin running? Is the password 'AcademyRootPassword' correct?")
    sys.exit(1)

# 3. Import App Models
try:
    sys.path.append(os.getcwd())
    from app.database import Base
    from app import models
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    print("✓ Database Tables Verified/Created")
except Exception as e:
    print(f"✗ MODEL ERROR: {e}")
    sys.exit(1)

# 4. Data Generation Functions
def generate_plate():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return f"TN{random.randint(10, 99)} {random.choice(letters)}{random.choice(letters)} {random.randint(1000, 9999)}"

# Route Data subset
routes = [
    ("1", "Broadway", "Thiruvotriyur"), ("1A", "Thiruvotriyur", "Thiruvanmiyur"),
    ("1D", "Ennore", "Thiruvanmiyur"), ("2A", "Anna Square", "K.K. Nagar"),
    ("3", "T. Nagar", "Thiruvanmiyur"), ("4", "Broadway", "Ennore"),
    ("5", "Broadway", "Adyar"), ("5B", "T. Nagar", "Mylapore"),
    ("5C", "Broadway", "Taramani"), ("5E", "Vadapalani", "Besant Nagar")
]

# 5. Populate
print(f"Starting to add 100 buses (10 per route)...")
total_added = 0

try:
    for route_num, start, end in routes:
        print(f"Adding 10 buses for Route {route_num}...", end="\r")
        for n in range(1, 11):
            bus_label = f"{route_num}-BUS-{n}"
            
            # Use random plate with CAPITAL letters
            plate = generate_plate()
            
            # Check if exists
            exists = db.query(models.Bus).filter(models.Bus.bus_number == bus_label).first()
            if not exists:
                new_bus = models.Bus(
                    bus_number=bus_label,
                    plate_number=plate,
                    bus_type="Ordinary" if n <= 5 else "Deluxe",
                    total_seats=40,
                    operator_name="LocoTranz"
                )
                db.add(new_bus)
                db.commit() # Get ID
                
                # Add Seats (Important!)
                for row in ['A', 'B', 'C', 'D']:
                    for s_num in range(1, 11):
                        seat = models.Seat(bus_id=new_bus.id, seat_label=f"{s_num}{row}", is_available=True)
                        db.add(seat)
                total_added += 1
        
        db.commit() # Commit after each route

    print(f"\n\n✓ SUCCESS! Total Buses Added: {total_added}")
    print("Check your pgAdmin now - the 'buses' table should be full.")

except Exception as e:
    db.rollback()
    print(f"\n✗ ERROR DURING POPULATION: {e}")
finally:
    db.close()
