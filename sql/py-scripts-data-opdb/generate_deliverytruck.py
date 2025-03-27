import csv
import random
import string

# Output CSV file name
output_file = "delivery_truck_data.csv"

# Define starting ID number (continue from existing data)
start_id = 85  # Since your last entry appears to be PDS-80TR
num_records = 500  # Generate 500 new records

# Define truck types and their weight ranges
truck_types = {
    "Van": (10, 1000),          # Weight range: 10-1000 lbs
    "Mini Truck": (100, 700),   # Weight range: 100-700 lbs
    "Cargo Truck": (400, 800),  # Weight range: 400-800 lbs
    "Heavy Truck": (300, 900)   # Weight range: 300-900 lbs
}

# Generate license plates
def generate_license_plate():
    # Format: 3 letters/numbers + space + 3 letters/numbers + space + 2 letters/numbers
    chars = string.ascii_uppercase + string.digits
    part1 = ''.join(random.choice(chars) for _ in range(3))
    part2 = ''.join(random.choice(chars) for _ in range(3))
    part3 = ''.join(random.choice(chars) for _ in range(2))
    return f"{part1} {part2} {part3}"

# Generate truck data
truck_data = []

for i in range(num_records):
    current_id = start_id + i
    
    # Generate truck ID (PDS-{ID}TR)
    dt_id = f"PDS-{current_id}TR"
    
    # Randomly select a truck type
    dt_type = random.choice(list(truck_types.keys()))
    
    # Generate maximum weight based on truck type
    min_weight, max_weight = truck_types[dt_type]
    dt_maximumwtinlbs = random.randint(min_weight, max_weight)
    
    # Generate license plate
    dt_licenseplate = generate_license_plate()
    
    # Add to data list
    truck_data.append({
        "dt_id": dt_id,
        "dt_type": dt_type,
        "dt_maximumwtinlbs": dt_maximumwtinlbs,
        "dt_licenseplate": dt_licenseplate
    })

# Write to CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ["dt_id", "dt_type", "dt_maximumwtinlbs", "dt_licenseplate"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for data in truck_data:
        writer.writerow(data)

print(f"Successfully generated CSV file with {len(truck_data)} new delivery truck records: {output_file}")
print(f"IDs range from {start_id} to {start_id + num_records - 1}")