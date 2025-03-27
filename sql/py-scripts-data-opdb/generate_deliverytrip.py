import csv
import random
import string
from sqlalchemy import create_engine, text

# Database connection string - update with your actual connection info
db_uri = "postgresql://username:pwdja123@localhost:5432/postal_delivery_system_db"

# Output CSV file name
output_file = "deliverytrip_data.csv"

# Define starting ID number (continue from existing data)
start_id = 16  # Since your last entry appears to be PDS-15TP-A
num_records = 10000  # How many new records to generate

# Connect to the database and fetch truck IDs and delivery person IDs
try:
    # Create engine and connect
    engine = create_engine(db_uri)
    
    with engine.connect() as connection:
        # Fetch all truck IDs from the deliverytruck table
        truck_result = connection.execute(text("SELECT dt_id FROM postal_delivery_system_opdb.deliverytruck"))
        truck_ids = [row[0] for row in truck_result.fetchall()]
        
        if not truck_ids:
            print("No truck IDs found in the database!")
            exit(1)
        
        # Fetch all delivery person IDs from the deliveryperson table
        person_result = connection.execute(text("SELECT dp_empid FROM postal_delivery_system_opdb.deliveryperson"))
        delivery_person_ids = [row[0] for row in person_result.fetchall()]
        
        if not delivery_person_ids:
            print("No delivery person IDs found in the database!")
            exit(1)
        
        print(f"Found {len(truck_ids)} trucks and {len(delivery_person_ids)} delivery persons in the database")
        
        # Define possible trip statuses
        trip_statuses = ["Completed", "In Progress", "Scheduled", "Delayed", "Cancelled"]
        status_weights = [0.6, 0.3, 0.05, 0.03, 0.02]  # 60% completed, 30% in progress, etc.
        
        # Generate tracking number
        def generate_tracking_number():
            # Format based on your existing data
            tracking_formats = [
                # 8 digits + dash + digit
                lambda: f"{random.randint(10000000, 99999999)}-{random.randint(1, 9)}",
                # 7 digits + dash + digit
                lambda: f"{random.randint(1000000, 9999999)}-{random.randint(1, 9)}",
                # 7 digits + dash + letter
                lambda: f"{random.randint(1000000, 9999999)}-{random.choice(string.ascii_uppercase)}",
                # 8 digits + dash + letter
                lambda: f"{random.randint(10000000, 99999999)}-{random.choice(string.ascii_uppercase)}"
            ]
            return random.choice(tracking_formats)()
        
        # Generate gas cost per mile
        def generate_gas_cost():
            # Based on your data, costs seem to range from $1.40 to $4.93
            return f"${random.uniform(1.40, 4.95):.2f}"
        
        # Generate delivery trip data
        trip_data = []
        used_tracking_numbers = set()
        
        for i in range(num_records):
            current_id = start_id + i
            
            # Generate trip ID (PDS-{ID}TP-A)
            dtrip_id = f"PDS-{current_id}TP-A"
            
            # Generate unique tracking number
            while True:
                tracking_no = generate_tracking_number()
                if tracking_no not in used_tracking_numbers:
                    used_tracking_numbers.add(tracking_no)
                    break
            
            # Randomly select a trip status based on weights
            dtrip_status = random.choices(trip_statuses, weights=status_weights)[0]
            
            # Randomly select a truck ID from the available truck IDs
            dtrip_truckid = random.choice(truck_ids)
            
            # Randomly select a delivery person ID from the available delivery person IDs
            dtrip_deliverypersonid = random.choice(delivery_person_ids)
            
            # Generate gas cost per mile
            gas_cost_per_mile = generate_gas_cost()
            
            # Add to data list
            trip_data.append({
                "dtrip_id": dtrip_id,
                "dtrip_trackingno": tracking_no,
                "dtrip_status": dtrip_status,
                "dtrip_truckid": dtrip_truckid,
                "dtrip_deliverypersonid": dtrip_deliverypersonid,
                "gas_cost_per_mile": gas_cost_per_mile
            })
        
        # Write to CSV file
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ["dtrip_id", "dtrip_trackingno", "dtrip_status", "dtrip_truckid", "dtrip_deliverypersonid", "gas_cost_per_mile"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in trip_data:
                writer.writerow(data)
        
        print(f"Successfully generated CSV file with {len(trip_data)} new delivery trip records: {output_file}")
        print(f"IDs range from {trip_data[0]['dtrip_id']} to {trip_data[-1]['dtrip_id']}")

except Exception as error:
    print(f"Error: {error}")