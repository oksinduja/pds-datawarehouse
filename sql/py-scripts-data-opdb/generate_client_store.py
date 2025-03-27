import csv
import random
from sqlalchemy import create_engine, text

# Database connection string - update with your actual connection info
db_uri = "postgresql://username:pwdja123@localhost:5432/postal_delivery_system_db"

# Output CSV file name
output_file = "client_store_data.csv"

# Create the engine
engine = create_engine(db_uri)

try:
    # Connect to the database
    with engine.connect() as connection:
        result = connection.execute(text(
            "SELECT client_id FROM postal_delivery_system_opdb.client WHERE client_id LIKE 'CLI-%-S'"
        ))
        store_clients = result.fetchall()
        
        # Create a list to hold all client store data
        client_store_data = []
        
        # Generate random warehouse status for each client
        for client in store_clients:
            client_id = client[0]
            # Randomly assign 'Yes' or 'No' for has_warehouse (60% Yes, 40% No)
            has_warehouse = 'Yes' if random.random() < 0.6 else 'No'
            
            # Add to our data list
            client_store_data.append({
                'client_id': client_id,
                'client_haswarehouse': has_warehouse
            })
        
        # Write to CSV file
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['client_id', 'client_haswarehouse']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in client_store_data:
                writer.writerow(data)
        
        print(f"Successfully generated CSV file with {len(client_store_data)} records: {output_file}")

except Exception as error:
    print("Error:", error)