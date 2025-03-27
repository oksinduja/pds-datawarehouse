import csv
import random
import string
from sqlalchemy import create_engine, text

# Database connection string - update with your actual connection info
db_uri = "postgresql://username:pwdja123@localhost:5432/postal_delivery_system_db"
# Output CSV file name
output_file = "deliverycomplaint_data.csv"

# Number of complaints to generate (approximately 5% of all orders)
complaint_ratio = 0.05  # 5% of orders will have complaints

# Connect to the database and fetch required data
try:
    # Create engine and connect
    engine = create_engine(db_uri)
    
    with engine.connect() as connection:
        # Fetch ONLY existing delivery order IDs from the database to ensure FK integrity
        order_result = connection.execute(text("""
            SELECT do_id, do_orderstatus 
            FROM postal_delivery_system_opdb.deliveryorder
            WHERE do_orderstatus LIKE 'Order Completed%'
            ORDER BY do_id
        """))
        orders = [(row[0], row[1]) for row in order_result.fetchall()]
        
        if not orders:
            print("No completed orders found in the database. Cannot generate complaints.")
            exit(1)
        
        # Determine the highest existing complaint ID number
        try:
            max_id_result = connection.execute(text("""
                SELECT MAX(CAST(REGEXP_REPLACE(dc_id, '[^0-9]+', '', 'g') AS INTEGER))
                FROM postal_delivery_system_opdb.deliverycomplaint
            """))
            max_id = max_id_result.fetchone()[0]
            complaint_id_counter = (max_id or 0) + 1
        except:
            complaint_id_counter = 31  # Start from a safe number (based on your previous data)
        
        print(f"Found {len(orders)} completed orders in the database")
        
        # Define possible complaint descriptions
        complaint_descriptions = [
            "Package Damaged",
            "Package Lost",
            "Delivery Delay",
            "Delivery Person Rude",
            "Wrong Delivery Location",
            "Package Opened",
            "Partial Delivery",
            "Delivery Attempt Failed",
            "No Delivery Notification",
            "Package Left Unattended"
        ]
        
        # Define possible statuses
        complaint_statuses = [
            "Pending",
            "Under Investigation",
            "Resolved"
        ]
        
        # Weights for statuses (making some more common than others)
        status_weights = [0.4, 0.4, 0.2]  # 40% Pending, 40% Under Investigation, 20% Resolved
        
        # Helper function to generate complaint ID
        def generate_complaint_id(counter):
            return f"PDS-{counter}CMP"
        
        # Generate complaints data
        complaints_data = []
        
        # Extract just the order IDs
        order_ids = [order_id for order_id, _ in orders]
        
        # Determine how many complaints to generate (minimum of 500, maximum of available orders)
        num_complaints = min(max(500, int(len(order_ids) * complaint_ratio)), len(order_ids))
        
        # Select random orders for complaints (without replacement)
        complaint_orders = random.sample(order_ids, num_complaints)
        
        # Generate complaints for selected orders
        for order_id in complaint_orders:
            # Generate complaint ID
            dc_id = generate_complaint_id(complaint_id_counter)
            
            # Randomly select a complaint description
            dc_desc = random.choice(complaint_descriptions)
            
            # Randomly select a status based on weights
            dc_status = random.choices(complaint_statuses, weights=status_weights)[0]
            
            # Add to data list
            complaints_data.append({
                "dc_id": dc_id,
                "dorder_id": order_id,
                "dc_desc": dc_desc,
                "dc_status": dc_status
            })
            
            complaint_id_counter += 1
        
        # Write to CSV file
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ["dc_id", "dorder_id", "dc_desc", "dc_status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in complaints_data:
                writer.writerow(data)
        
        # Additionally, output an SQL file for direct import
        sql_file = output_file.replace('.csv', '.sql')
        with open(sql_file, 'w') as f:
            f.write("-- SQL Insert statements for deliverycomplaint table\n\n")
            
            for data in complaints_data:
                sql = f"INSERT INTO postal_delivery_system_opdb.deliverycomplaint (dc_id, dorder_id, dc_desc, dc_status) VALUES ('{data['dc_id']}', '{data['dorder_id']}', '{data['dc_desc']}', '{data['dc_status']}');\n"
                f.write(sql)
        
        print(f"Successfully generated CSV file with {len(complaints_data)} delivery complaint records: {output_file}")
        print(f"Also generated SQL file for direct import: {sql_file}")
        print(f"Complaint IDs range from {complaints_data[0]['dc_id']} to {complaints_data[-1]['dc_id']}")

except Exception as error:
    print(f"Error: {error}")