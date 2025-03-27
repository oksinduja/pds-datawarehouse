import csv
import random
import string
from datetime import datetime, timedelta

# Output CSV file name
output_file = "deliveryperson_data.csv"

# Define starting ID number (continue from existing data)
start_id = 21  # Since your last entry appears to be PDS-20-EMP
num_records = 500  # Generate 100 new records (adjust as needed)

# Generate license number
def generate_license_number():
    chars = string.ascii_uppercase + string.digits
    part1 = ''.join(random.choice(chars) for _ in range(3))
    part2 = ''.join(random.choice(chars) for _ in range(3))
    part3 = ''.join(random.choice(chars) for _ in range(3))
    return f"{part1} {part2} {part3}"

# Generate random date between 2020-01-01 and now
def generate_join_date():
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

# Generate random hourly wage between $5.00 and $10.00
def generate_hourly_wage():
    wage = round(random.uniform(5.00, 10.00), 2)
    return f"${wage:.2f} per hour"

# Generate delivery person data
deliveryperson_data = []

for i in range(num_records):
    current_id = start_id + i
    
    # Generate employee ID (PDS-{ID}-EMP)
    dp_empid = f"PDS-{current_id}-EMP"
    
    # Generate manager ID (PDS-{ID}-MG)
    dp_managerid = f"PDS-{current_id}-MG"
    
    # Generate join date
    dp_joindate = generate_join_date()
    
    # Generate license number
    dp_licenseno = generate_license_number()
    
    # Generate can drive heavy truck (Yes/No)
    dp_candriveheavytruck = "Yes" if random.random() < 0.5 else "No"
    
    # Generate can drive out of state (Yes/No)
    dp_candriveoutstate = "Yes" if random.random() < 0.6 else "No"
    
    # Generate base salary
    dp_basesalary = generate_hourly_wage()
    
    # Add to data list
    deliveryperson_data.append({
        "dp_empid": dp_empid,
        "dp_managerid": dp_managerid,
        "dp_joindate": dp_joindate,
        "dp_licenseno": dp_licenseno,
        "dp_candriveheavytruck": dp_candriveheavytruck,
        "dp_candriveoutstate": dp_candriveoutstate,
        "dp_basesalary": dp_basesalary
    })

# Write to CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ["dp_empid", "dp_managerid", "dp_joindate", "dp_licenseno", 
                  "dp_candriveheavytruck", "dp_candriveoutstate", "dp_basesalary"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for data in deliveryperson_data:
        writer.writerow(data)

print(f"Successfully generated CSV file with {len(deliveryperson_data)} new delivery person records: {output_file}")
print(f"IDs range from PDS-{start_id}-EMP to PDS-{start_id + num_records - 1}-EMP")