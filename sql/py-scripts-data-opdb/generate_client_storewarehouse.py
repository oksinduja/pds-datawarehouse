import csv
import random
from sqlalchemy import create_engine, text

# Database connection string - update with your actual connection info
db_uri = "postgresql://username:pwdja123@localhost:5432/postal_delivery_system_db"
# Output CSV file name
output_file = "client_storewarehouse_data.csv"

# Create the engine
engine = create_engine(db_uri)

try:
    # Connect to the database
    with engine.connect() as connection:
        # Fetch all clients from client_store table that have warehouses
        result = connection.execute(text(
            "SELECT client_id FROM postal_delivery_system_opdb.client_store WHERE client_haswarehouse = 'Yes'"
        ))
        clients_with_warehouses = [row[0] for row in result.fetchall()]
        
        if not clients_with_warehouses:
            print("No clients with warehouses found in the client_store table!")
            exit(1)
            
        print(f"Found {len(clients_with_warehouses)} clients with warehouses in the client_store table")
        
        # Generate warehouse data for each client
        client_storewarehouse_data = []
        
        # Keep track of used warehouse IDs to avoid duplicates
        used_wh_numbers = set()
        
        for client_id in clients_with_warehouses:
            # Decide how many warehouses this client has (1-3)
            num_warehouses = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
            
            warehouse_count = 0
            attempts = 0
            max_attempts = 50  # Prevent infinite loops
            
            while warehouse_count < num_warehouses and attempts < max_attempts:
                attempts += 1
                
                # Generate a unique warehouse number
                wh_number = random.randint(1, 100000)
                if wh_number in used_wh_numbers:
                    continue  # Skip this iteration if the number is already used
                
                used_wh_numbers.add(wh_number)
                warehouse_count += 1
                
                # Generate warehouse ID (WH + number + -S suffix)
                sw_id = f"WH{wh_number}-S"
                
                # Generate random capacity between 1000-2500
                sw_capacity = random.randint(1000, 2500)
                
                # Generate random worker count between 20-50
                sw_noofworkers = random.randint(20, 200)
                
                # Generate supervisor ID based on warehouse ID
                sw_supervisorid = f"WH-{wh_number}SUP-{wh_number}"
                
                # Generate supervisor name
                first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", 
                              "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan"]
                last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", 
                             "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White"]
                sw_supervisorname = f"{random.choice(first_names)} {random.choice(last_names)}"
                
                client_storewarehouse_data.append({
                    "client_id": client_id,
                    "sw_id": sw_id,
                    "sw_capacity": sw_capacity,
                    "sw_noofworkers": sw_noofworkers,
                    "sw_supervisorid": sw_supervisorid,
                    "sw_supervisorname": sw_supervisorname,
                    "client_haswarehouse": "Yes"
                })
        
        # Write to CSV file
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ["client_id", "sw_id", "sw_capacity", "sw_noofworkers", 
                         "sw_supervisorid", "sw_supervisorname", "client_haswarehouse"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in client_storewarehouse_data:
                writer.writerow(data)
        
        print(f"Successfully generated CSV file with {len(client_storewarehouse_data)} records: {output_file}")
        print(f"Generated for {len(clients_with_warehouses)} clients with warehouses")
        print(f"Total unique warehouses: {len(used_wh_numbers)}")

except Exception as error:
    print("Error:", error)