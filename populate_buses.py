
import sys
import os
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add the current directory to sys.path so we can import from 'app'
sys.path.append(os.getcwd())

from app.database import SessionLocal, engine
from app import models

def generate_plate():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return f"TN{random.randint(10, 99)} {random.choice(letters)}{random.choice(letters)} {random.randint(1000, 9999)}"

def populate():
    db = SessionLocal()
    
    routes_data = [
        ("1", "Broadway", "Thiruvotriyur", (5, 12), (11, 25)),
        ("1A", "Thiruvotriyur", "Thiruvanmiyur", (5, 20), (11, 40)),
        ("1D", "Ennore", "Thiruvanmiyur", (5, 24), (11, 45)),
        ("2A", "Anna Square", "K.K. Nagar", (5, 15), (11, 30)),
        ("3", "T. Nagar", "Thiruvanmiyur", (5, 10), (11, 20)),
        ("4", "Broadway", "Ennore", (5, 18), (11, 35)),
        ("5", "Broadway", "Adyar", (5, 12), (11, 25)),
        ("5B", "T. Nagar", "Mylapore", (5, 7), (11, 15)),
        ("5C", "Broadway", "Taramani", (5, 15), (11, 30)),
        ("5E", "Vadapalani", "Besant Nagar", (5, 14), (11, 28)),
        ("7B", "Broadway", "Korattur", (5, 14), (11, 28)),
        ("7H", "Broadway", "JJ Nagar East", (5, 15), (11, 30)),
        ("7K", "T. Nagar", "Taramani", (5, 10), (11, 20)),
        ("7M", "Broadway", "JJ Nagar West", (5, 16), (11, 32)),
        ("8", "Broadway", "Perambur", (5, 10), (11, 20)),
        ("9", "Broadway", "T. Nagar", (5, 10), (11, 20)),
        ("9M", "T. Nagar", "AGS Office Colony", (5, 12), (11, 25)),
        ("10", "Broadway", "T. Nagar", (5, 10), (11, 20)),
        ("10A", "Tollgate", "Saidapet West", (5, 14), (11, 28)),
        ("11", "Broadway", "T. Nagar", (5, 10), (11, 20)),
        ("11A", "Vallalar Nagar", "T. Nagar", (5, 11), (11, 22)),
        ("12", "T. Nagar", "Vivekananda House", (5, 8), (11, 18)),
        ("12B", "Vadapalani", "Foreshore Estate", (5, 12), (11, 25)),
        ("13", "T. Nagar", "Triplicane", (5, 8), (11, 18)),
        ("14", "Broadway", "Arumbakkam", (5, 12), (11, 25)),
        ("15", "Broadway", "Anna Nagar West", (5, 13), (11, 26)),
        ("15F", "Vadapalani", "Broadway", (5, 12), (11, 25)),
        ("15G", "MMDA Colony", "Broadway", (5, 11), (11, 22)),
        ("17", "Broadway", "Vadapalani", (5, 12), (11, 25)),
        ("18", "Broadway", "Saidapet", (5, 10), (11, 20)),
        ("18A", "Broadway", "Kilambakkam (KCBT)", (5, 24), (11, 48)),
        ("18D", "Broadway", "Keelkattalai", (5, 18), (11, 35)),
        ("19", "T. Nagar", "Thiruporur", (5, 24), (11, 50)),
        ("19B", "Saidapet", "Kelambakkam", (5, 22), (11, 45)),
        ("19C", "T. Nagar", "Sholinganallur", (5, 18), (11, 35)),
        ("20", "Broadway", "Villivakkam", (5, 12), (11, 25)),
        ("20A", "Broadway", "JJ Nagar East", (5, 15), (11, 30)),
        ("21", "Broadway", "Mandaveli", (5, 10), (11, 20)),
        ("21G", "Broadway", "Kilambakkam (KCBT)", (5, 24), (11, 48)),
        ("22", "Ayanavaram", "Anna Square", (5, 11), (11, 22)),
        ("23C", "Ayanavaram", "Besant Nagar", (5, 15), (11, 30)),
        ("25", "Vadapalani", "Triplicane", (5, 11), (11, 22)),
        ("26", "T. Nagar", "ICF", (5, 11), (11, 22)),
        ("27B", "Anna Square", "CMBT (Koyambedu)", (5, 14), (11, 28)),
        ("28", "Thiruvotriyur", "Egmore R.S.", (5, 14), (11, 28)),
        ("28B", "Ennore", "Egmore North R.S.", (5, 18), (11, 35)),
        ("29C", "Perambur", "Besant Nagar", (5, 16), (11, 32)),
        ("32", "Vallalar Nagar", "Vivekananda House", (5, 8), (11, 18)),
        ("33", "MKB Nagar", "Broadway", (5, 9), (11, 20)),
        ("34", "Thiruvotriyur", "Ambattur I.E.", (5, 20), (11, 40)),
        ("37", "Iyyappanthangal", "Vallalar Nagar", (5, 18), (11, 35)),
        ("37B", "JJ Nagar West", "Vallalar Nagar", (5, 15), (11, 30)),
        ("38A", "Broadway", "Mathur MMDA", (5, 15), (11, 30)),
        ("38H", "Broadway", "Mathur MMDA", (5, 15), (11, 30)),
        ("40", "Anna Square", "Ambattur O.T.", (5, 18), (11, 35)),
        ("41C", "Thiruvanmiyur", "Anna Nagar West", (5, 18), (11, 35)),
        ("42", "Broadway", "Periyar Nagar", (5, 12), (11, 25)),
        ("44", "Broadway", "Manali", (5, 16), (11, 32)),
        ("45B", "Anna Square", "Guindy TVK Estate", (5, 12), (11, 25)),
        ("46", "CMBT", "T. Nagar", (5, 10), (11, 20)),
        ("47", "Adyar", "Villivakkam", (5, 16), (11, 32)),
        ("47A", "Besant Nagar", "Villivakkam", (5, 18), (11, 35)),
        ("47C", "Kotturpuram", "Ambattur I.E.", (5, 18), (11, 35)),
        ("48A", "Ambattur I.E.", "Madhavaram", (5, 15), (11, 30)),
        ("49", "Tiruvanmiyur", "Iyyappanthangal", (5, 18), (11, 35)),
        ("50", "Broadway", "Poonamallee", (5, 20), (11, 40)),
        ("51", "Velachery", "Tambaram West", (5, 15), (11, 30)),
        ("51H", "Saidapet", "Tambaram East", (5, 18), (11, 35)),
        ("54", "Broadway", "Poonamallee", (5, 20), (11, 40)),
        ("57", "Broadway", "Red Hills", (5, 18), (11, 35)),
        ("62", "Red Hills", "Poonamallee", (5, 22), (11, 45)),
        ("66", "Tambaram", "Poonamallee", (5, 18), (11, 35)),
        ("70", "Avadi", "Tambaram", (5, 24), (11, 50)),
        ("70H", "CMBT", "Hasthinapuram", (5, 20), (11, 40)),
        ("70W", "JJ Nagar West", "Velachery", (5, 20), (11, 40)),
        ("77", "CMBT", "Ambattur Estate", (5, 10), (11, 20)),
        ("78", "Thiruvanmiyur", "CMBT", (5, 16), (11, 32)),
        ("88C", "Broadway", "Kundrathur", (5, 22), (11, 45)),
        ("91", "CMBT", "Thiruvanmiyur", (5, 16), (11, 32)),
        ("95", "Tambaram East", "Thiruvanmiyur", (5, 18), (11, 35)),
        ("99", "Tambaram West", "Adyar", (5, 20), (11, 40)),
        ("101", "Thiruvotriyur", "Poonamallee", (5, 24), (11, 50)),
        ("102", "Broadway", "Kelambakkam", (5, 24), (11, 50)),
        ("104", "Red Hills", "CMBT", (5, 18), (11, 35)),
        ("104A", "Avadi", "Kilambakkam (KCBT)", (5, 24), (11, 50)),
        ("105", "Tambaram West", "Siruseri IT Park", (5, 20), (11, 40)),
        ("114", "Red Hills", "Tambaram", (5, 24), (11, 50)),
        ("119", "Guindy", "Chemmanchery", (5, 18), (11, 35)),
        ("121C", "Ennore", "CMBT", (5, 22), (11, 45)),
        ("121G", "KK Nagar", "CMBT", (5, 10), (11, 20)),
        ("142", "Perambur", "Vinayagapuram", (5, 10), (11, 20)),
        ("150", "Broadway", "Red Hills", (5, 18), (11, 35)),
        ("153", "CMBT", "Thiruvallur", (5, 24), (11, 55)),
        ("154", "T. Nagar", "Poonamallee", (5, 18), (11, 35)),
        ("170", "CMBT", "Tambaram", (5, 20), (11, 42)),
        ("202", "Tambaram", "Avadi", (5, 24), (11, 50)),
        ("500", "T. Nagar", "Chengalpattu", (10, 35), (25, 75)),
        ("500A", "Hasthinapuram", "Chengalpattu", (10, 30), (25, 65)),
        ("570", "CMBT", "Kelambakkam", (5, 24), (11, 50)),
        ("588", "Adyar", "Mamallapuram", (15, 40), (35, 85))
    ]

    print(f"Starting population of {len(routes_data)} routes...")

    bus_count = 0
    sched_count = 0
    
    # Batch size to avoid memory issues or transaction timeouts
    batch_size = 50
    
    for i, (route_num, start, end, ord_range, del_range) in enumerate(routes_data):
        # Create 5 Ordinary and 5 Deluxe buses for each route
        types = [
            ("Ordinary", ord_range, "LocoTranz Ordinary"),
            ("Deluxe", del_range, "LocoTranz Deluxe")
        ]
        
        for b_type, price_range, operator in types:
            for n in range(1, 6): # 5 buses each
                bus_label = f"{route_num}-{b_type[0]}-{n}"
                plate = generate_plate()
                
                # Check if bus already exists (unique constraint)
                existing_bus = db.query(models.Bus).filter(models.Bus.bus_number == bus_label).first()
                if not existing_bus:
                    new_bus = models.Bus(
                        bus_number=bus_label,
                        plate_number=plate,
                        bus_type=b_type,
                        total_seats=40,
                        operator_name=operator
                    )
                    db.add(new_bus)
                    db.flush() # Get the bus ID
                    
                    # Create 40 seats for this bus
                    seats_to_add = []
                    for row in ['A', 'B', 'C', 'D']:
                        for num in range(1, 11):
                            seat = models.Seat(
                                bus_id=new_bus.id,
                                seat_label=f"{num}{row}",
                                is_available=True
                            )
                            seats_to_add.append(seat)
                    db.bulk_save_objects(seats_to_add)
                    
                    # Create a schedule for this bus
                    dep_time = datetime.now() + timedelta(hours=random.randint(1, 48), minutes=random.choice([0, 15, 30, 45]))
                    arr_time = dep_time + timedelta(hours=random.randint(1, 3))
                    
                    price = random.randint(price_range[0], price_range[1])
                    
                    schedule = models.Schedule(
                        bus_id=new_bus.id,
                        source=start,
                        destination=end,
                        departure_time=dep_time,
                        arrival_time=arr_time,
                        price=float(price),
                        available_seats=40,
                        status="Scheduled",
                        route_id=route_num
                    )
                    db.add(schedule)
                    
                    bus_count += 1
                    sched_count += 1
        
        # Commit every batch of routes
        db.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Processed route {route_num} ({i+1}/{len(routes_data)})")

    db.commit()
    print(f"Finished! Total buses added: {bus_count}, Total schedules added: {sched_count}")
    db.close()

if __name__ == "__main__":
    populate()
