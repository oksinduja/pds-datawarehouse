import csv
import random
import string
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# Database connection string - update with your actual connection info
db_uri = "postgresql://username:pwdja123@localhost:5432/postal_delivery_system_db"

# Output CSV file name
output_file = "deliveryorder_data.csv"

# Number of orders to generate
num_orders = 50000

# Connect to the database and fetch required data
try:
    # Create engine and connect
    engine = create_engine(db_uri)
    
    with engine.connect() as connection:
        # Fetch all clients with their join dates
        client_result = connection.execute(text("""
            SELECT client_id, client_datejoined, client_zipcode, client_city 
            FROM postal_delivery_system_opdb.client
            ORDER BY client_id
        """))
        clients = [{"client_id": row[0], 
                   "join_date": datetime.strptime(row[1], '%m-%d-%Y'),
                   "zipcode": row[2],
                   "city": row[3]} 
                 for row in client_result.fetchall()]
        
        # Fetch all delivery trips with their status
        trip_result = connection.execute(text("""
            SELECT dtrip_id, dtrip_status
            FROM postal_delivery_system_opdb.deliverytrip
            ORDER BY dtrip_id
        """))
        trips = [{"trip_id": row[0], "status": row[1]} 
                for row in trip_result.fetchall()]
        
        # Create region mapping (group cities/zipcodes by region)
        # Group cities into regions based on first digit of zipcode
        regions = {}
        for client in clients:
            zipcode = client["zipcode"]
            if zipcode and len(zipcode) >= 1:
                region_key = zipcode[0]  # First digit of zipcode
                if region_key not in regions:
                    regions[region_key] = []
                if client["city"] and client["city"] not in regions[region_key]:
                    regions[region_key].append(client["city"])
        
        print(f"Found {len(clients)} clients, {len(trips)} trips, and {len(regions)} regions")
        
        # Helper functions
        def generate_order_id(index):
            # Format: OR-{NUMBER}-DL
            return f"OR-{index}-DL"
        
        def generate_tracking_number():
            length = random.randint(12, 16)
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        
        def generate_address():
            street_numbers = ["123", "456", "789", "1011", "1213", "1415", "1617", "1819", "2021", "2223"]
            street_types = [
        "St.", "St", "Street", "Ave.", "Ave", "Avenue", "Blvd.", "Blvd", "Boulevard", "Rd.", "Rd", "Road",
        "Ln.", "Ln", "Lane", "Dr.", "Dr", "Drive", "Way", "Place", "Pl.", "Ct.", "Ct", "Court"
    ]
            street_names = [
                "Main", "Oak", "Pine", "Maple", "Cedar", "Elm", "Washington", "Park", "Lake", "Hill",
                "River", "View", "Ridge", "Forest", "High", "Meadow", "Valley", "Spring", "Sunset", "Sunrise",
                "Market", "Church", "Mill", "Bridge", "First", "Second", "Third", "Fourth", "Fifth", "Sixth",
                "Highland", "Lincoln", "Jackson", "Franklin", "Adams", "Jefferson", "Madison", "Wilson", "Monroe", "Grant",
                "Central", "Broadway", "Railroad", "Water", "College", "Columbia", "Pearl", "Walnut", "Chestnut", "Cherry"
            ]
            
            address_types = [
                f"{random.choice(street_numbers)} {random.choice(street_names)} {random.choice(street_types)}",
                f"P.O. Box {random.randint(100, 999)}, {random.choice(street_names)} {random.choice(street_types)}",
                f"Apt #{random.randint(100, 999)}, {random.choice(street_names)} {random.choice(street_types)}"
            ]
            
            return random.choice(address_types)
        
        def generate_phone():
            formats = [
                "({area}) {prefix}-{line}",
                "{area}-{prefix}-{line}",
                "1-{area}-{prefix}-{line}"
            ]
            
            area_code = random.randint(201, 989)
            prefix = random.randint(200, 999)
            line = random.randint(1000, 9999)
            
            chosen_format = random.choice(formats)
            return chosen_format.format(area=area_code, prefix=prefix, line=line)
        
        def generate_payment_cost():
            # Generate a realistic payment amount
            base = random.uniform(5, 500)
            return f"${base:.2f}"
        
        def generate_order_status(trip_status):
            # Map trip status to order status
            if trip_status == "Completed":
                return "Order Completed - Delivered"
            elif trip_status == "In Progress":
                statuses = ["On the way to delivery", "Delivery Processing"]
                return random.choice(statuses)
            else:  # Scheduled, Delayed, Cancelled
                return "Delivery Processing"
        
        # Determine the highest existing order ID number
        try:
            # Try to get the largest existing order ID
            max_id_result = connection.execute(text("""
                SELECT MAX(CAST(REGEXP_REPLACE(do_id, '[^0-9]+', '', 'g') AS INTEGER))
                FROM postal_delivery_system_opdb.deliveryorder
            """))
            max_id = max_id_result.fetchone()[0]
            if max_id:
                order_id_counter = max_id + 1
            else:
                order_id_counter = 200  # Start from a safe number
        except:
            # If that doesn't work, start from a safe number
            order_id_counter = 200
        
        # Assign each trip to a specific date range and region
        trip_assignments = {}
        used_date_regions = set()  # To track date-region combinations already assigned
        
        # Helper to generate a date range for a trip
        def get_trip_date_range():
            # Generate a random date between 2020-01-01 and 2024-12-31
            start_year = random.randint(2020, 2024)
            start_month = random.randint(1, 12)
            start_day = random.randint(1, 28)  # Safe for all months
            
            start_date = datetime(start_year, start_month, start_day)
            
            # Generate a date range of 1-5 days
            range_days = random.randint(1, 5)
            end_date = start_date + timedelta(days=range_days)
            
            return (start_date, end_date)
        
        # Generate unique trip assignments (date range + region)
        for trip in trips:
            assigned = False
            attempts = 0
            
            while not assigned and attempts < 50:
                attempts += 1
                date_range = get_trip_date_range()
                region_key = random.choice(list(regions.keys()))
                
                # Create a unique identifier for this date-region combination
                date_region_key = (date_range[0].strftime("%Y-%m-%d"), region_key)
                
                if date_region_key not in used_date_regions:
                    used_date_regions.add(date_region_key)
                    trip_assignments[trip["trip_id"]] = {
                        "trip": trip,
                        "start_date": date_range[0],
                        "end_date": date_range[1],
                        "region": region_key,
                        "orders": []
                    }
                    assigned = True
            
            # If we couldn't find a unique combination after 50 attempts, just assign anyway
            if not assigned:
                date_range = get_trip_date_range()
                region_key = random.choice(list(regions.keys()))
                trip_assignments[trip["trip_id"]] = {
                    "trip": trip,
                    "start_date": date_range[0],
                    "end_date": date_range[1],
                    "region": region_key,
                    "orders": []
                }
        
        # Generate orders for all trips first (minimum 7 per trip)
        order_data = []
        
        # First pass: ensure each trip has at least 7 orders
        for trip_id, assignment in trip_assignments.items():
            # Number of orders for this trip (7-15)
            num_trip_orders = random.randint(7, 15)
            
            # Find clients in this region
            region_clients = [client for client in clients 
                             if client["zipcode"] and client["zipcode"].startswith(assignment["region"])]
            
            # If no clients in this region, use any clients
            if not region_clients:
                region_clients = clients
            
            # Generate orders for this trip
            for i in range(num_trip_orders):
                # Select a random client from the region
                client = random.choice(region_clients)
                client_id = client["client_id"]
                client_join_date = client["join_date"]
                
                # Select a delivery date within the trip's date range but after client join date
                if client_join_date < assignment["end_date"]:
                    # Calculate valid date range
                    start_date = max(client_join_date, assignment["start_date"])
                    end_date = assignment["end_date"]
                    
                    # Generate a random date in the valid range
                    days_diff = (end_date - start_date).days
                    if days_diff > 0:
                        order_date = start_date + timedelta(days=random.randint(0, days_diff))
                    else:
                        order_date = start_date
                else:
                    # If client joined after trip end date, adjust the trip date
                    # This is an edge case but we'll handle it
                    order_date = client_join_date + timedelta(days=1)
                    assignment["end_date"] = order_date + timedelta(days=1)
                
                # Ensure order date is not in the future
                if order_date > datetime.now():
                    order_date = datetime.now() - timedelta(days=1)
                
                # Format the order date as a string
                order_date_str = order_date.strftime("%Y-%m-%d")
                
                # Use client's zipcode and city
                delivery_zipcode = client["zipcode"]
                delivery_city = client["city"]
                
                # Get trip status and determine order status
                trip_status = assignment["trip"]["status"]
                order_status = generate_order_status(trip_status)
                
                # Set completion date based on status
                if order_status == "Order Completed - Delivered":
                    # Completion date is 1-5 days after order date
                    completion_date = (order_date + timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
                else:
                    completion_date = None
                
                # Set estimated completion date (always 10 days after order date)
                est_completion_date = (order_date + timedelta(days=10)).strftime("%Y-%m-%d")
                
                # Generate other fields
                delivery_location = generate_address()
                delivery_phone = generate_phone()
                client_payment_cost = generate_payment_cost()
                weight_in_lbs = random.randint(1, 1000)
                tracking_number = generate_tracking_number()
                delivery_code = random.randint(1000, 9999)
                
                # Create the order record
                order = {
                    "do_id": generate_order_id(order_id_counter),
                    "do_date": order_date_str,
                    "do_deliverylocation": delivery_location,
                    "do_deliverycity": delivery_city,
                    "do_deliveryzipcode": delivery_zipcode,
                    "do_deliveryphone": delivery_phone,
                    "do_clientpaymentcost": client_payment_cost,
                    "do_orderstatus": order_status,
                    "do_weightinlbsrounded": weight_in_lbs,
                    "do_clientid": client_id,
                    "client_tracking_no": tracking_number,
                    "delivery_code": delivery_code,
                    "dtrip_id": trip_id,
                    "do_completiondate": completion_date,
                    "do_est_completiondate": est_completion_date
                }
                
                order_data.append(order)
                assignment["orders"].append(order_id_counter)
                order_id_counter += 1
        
        # Calculate remaining orders to generate
        remaining_orders = num_orders - len(order_data)
        
        # Second pass: Generate remaining orders, distribute to trips based on region and date
        for i in range(remaining_orders):
            # Select a random client
            client = random.choice(clients)
            client_id = client["client_id"]
            client_join_date = client["join_date"]
            client_region = client["zipcode"][0] if client["zipcode"] and len(client["zipcode"]) > 0 else None
            
            # Select a random order date after client join date
            max_days_since_join = (datetime.now() - client_join_date).days
            days_since_join = random.randint(1, max(1, max_days_since_join))
            order_date = client_join_date + timedelta(days=days_since_join)
            
            # Find trips that match this region and date
            compatible_trips = []
            for trip_id, assignment in trip_assignments.items():
                if assignment["region"] == client_region and assignment["start_date"] <= order_date <= assignment["end_date"]:
                    compatible_trips.append((trip_id, assignment))
            
            # 90% of orders get assigned to compatible trips if available
            if compatible_trips and random.random() < 0.9:
                # Sort by number of orders to prioritize trips with fewer orders
                compatible_trips.sort(key=lambda x: len(x[1]["orders"]))
                selected_trip_id, assignment = compatible_trips[0]
                
                # Set trip-related fields
                trip_status = assignment["trip"]["status"]
                order_status = generate_order_status(trip_status)
                
                # Set completion date based on status
                if order_status == "Order Completed - Delivered":
                    # Completion date is 1-5 days after order date
                    completion_date = (order_date + timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
                else:
                    completion_date = None
                
                trip_id = selected_trip_id
            else:
                # No compatible trip or in the 10% case - create order without trip
                order_status = "Delivery Processing"
                completion_date = None
                trip_id = None
            
            # Format the order date as a string
            order_date_str = order_date.strftime("%Y-%m-%d")
            
            # Set estimated completion date (always 10 days after order date)
            est_completion_date = (order_date + timedelta(days=10)).strftime("%Y-%m-%d")
            
            # Generate other fields
            delivery_location = generate_address()
            delivery_city = client["city"]
            delivery_zipcode = client["zipcode"]
            delivery_phone = generate_phone()
            client_payment_cost = generate_payment_cost()
            weight_in_lbs = random.randint(1, 1000)
            tracking_number = generate_tracking_number()
            delivery_code = random.randint(1000, 9999)
            
            # Create the order record
            order = {
                "do_id": generate_order_id(order_id_counter),
                "do_date": order_date_str,
                "do_deliverylocation": delivery_location,
                "do_deliverycity": delivery_city,
                "do_deliveryzipcode": delivery_zipcode,
                "do_deliveryphone": delivery_phone,
                "do_clientpaymentcost": client_payment_cost,
                "do_orderstatus": order_status,
                "do_weightinlbsrounded": weight_in_lbs,
                "do_clientid": client_id,
                "client_tracking_no": tracking_number,
                "delivery_code": delivery_code,
                "dtrip_id": trip_id,
                "do_completiondate": completion_date,
                "do_est_completiondate": est_completion_date
            }
            
            order_data.append(order)
            if trip_id:
                trip_assignments[trip_id]["orders"].append(order_id_counter)
            order_id_counter += 1
        
        # Write to CSV file
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ["do_id", "do_date", "do_deliverylocation", "do_deliverycity", 
                         "do_deliveryzipcode", "do_deliveryphone", "do_clientpaymentcost",
                         "do_orderstatus", "do_weightinlbsrounded", "do_clientid", 
                         "client_tracking_no", "delivery_code", "dtrip_id",
                         "do_completiondate", "do_est_completiondate"]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for data in order_data:
                writer.writerow(data)
        
        # Print statistics
        trips_with_orders = sum(1 for trip_id, assignment in trip_assignments.items() if len(assignment["orders"]) > 0)
        orders_with_trips = sum(1 for order in order_data if order["dtrip_id"] is not None)
        orders_without_trips = sum(1 for order in order_data if order["dtrip_id"] is None)
        
        print(f"Successfully generated CSV file with {len(order_data)} delivery order records: {output_file}")
        print(f"Orders with assigned trips: {orders_with_trips} ({orders_with_trips/len(order_data)*100:.1f}%)")
        print(f"Orders without trips (Delivery Processing): {orders_without_trips} ({orders_without_trips/len(order_data)*100:.1f}%)")
        print(f"Trips with assigned orders: {trips_with_orders} ({trips_with_orders/len(trips)*100:.1f}%)")
        
        # Calculate average orders per trip (for trips that have orders)
        if trips_with_orders > 0:
            orders_per_trip = [len(assignment["orders"]) for trip_id, assignment in trip_assignments.items() if len(assignment["orders"]) > 0]
            avg_orders = sum(orders_per_trip) / trips_with_orders
            min_orders = min(orders_per_trip)
            max_orders = max(orders_per_trip)
            
            print(f"Average orders per trip: {avg_orders:.1f}")
            print(f"Min orders per trip: {min_orders}, Max orders per trip: {max_orders}")

except Exception as error:
    print(f"Error: {error}")