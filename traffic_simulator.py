import time
import random
import datetime
from pymongo import MongoClient

# --- CONFIGURATION ---
# Replace with your MongoDB Connection String if using Atlas
MONGO_URI = "mongodb://localhost:27017/" 
DB_NAME = "TrafficManagementDB"
COLLECTION_NAME = "RealTimeTraffic"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Simulation Parameters
LOCATIONS = ["Main St & 1st Ave", "Broadway & 42nd", "Queens Blvd Exit 5"]

def generate_traffic_data():
    """Simulates a payload from a traffic sensor API."""
    current_time = datetime.datetime.now()
    
    data_batch = []
    for location in LOCATIONS:
        # Simulate random traffic patterns
        vehicle_count = random.randint(5, 150) # Cars per minute
        avg_speed = random.randint(10, 80)     # km/h
        
        # Logic: High traffic = Low speed
        if vehicle_count > 100:
            avg_speed = random.randint(5, 25)
            congestion_level = "High"
        elif vehicle_count > 50:
            avg_speed = random.randint(25, 50)
            congestion_level = "Moderate"
        else:
            avg_speed = random.randint(50, 80)
            congestion_level = "Low"

        record = {
            "timestamp": current_time,
            "location": location,
            "vehicle_count": vehicle_count,
            "avg_speed": avg_speed,
            "congestion_level": congestion_level,
            "sensor_id": f"Sens-{location[0:3].upper()}-{random.randint(100,999)}"
        }
        data_batch.append(record)
    
    return data_batch

def main():
    print(f"🚗 Starting Traffic Simulation API... Pushing to DB: {DB_NAME}")
    try:
        while True:
            traffic_data = generate_traffic_data()
            collection.insert_many(traffic_data)
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Inserted {len(traffic_data)} records.")
            
            # Wait 3 seconds before next update (Simulates real-time)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n🛑 Simulation Stopped.")

if __name__ == "__main__":
    main()