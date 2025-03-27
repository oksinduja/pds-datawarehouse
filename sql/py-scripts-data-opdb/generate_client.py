import random
import string
from datetime import datetime, timedelta
import csv

def generate_client_id(index):
    # Only allow P and S suffixes
    # P suffix starts from 81, S suffix starts from 21
    if random.random() < 0.5:  # 50% chance of P
        number = 80 + index  # Start from 81
        suffix = "P"
    else:  # 50% chance of S
        number = 20 + index  # Start from 21
        suffix = "S"
    
    return f"CLI-{number}-{suffix}"

def generate_zipcode():
    return str(random.randint(10000, 99999))

def generate_name():
    first_names = [
        "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
        "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
        "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra",
        "Donald", "Ashley", "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
        "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Edward", "Deborah",
        "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon", "Jeffrey", "Laura", "Ryan", "Cynthia",
        "Jacob", "Kathleen", "Gary", "Amy", "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen",
        "Stephen", "Anna", "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
        "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
        "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King",
        "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
        "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins",
        "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey",
        "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez",
        "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross"
    ]
    
    company_prefixes = [
        "Advanced", "Allied", "American", "Associated", "Blue Sky", "Capital", "Central", "Century", "City", "Coastal",
        "Creative", "Crystal", "Diamond", "Digital", "Dynamic", "Eagle", "East Coast", "Eastern", "Elite", "Emerald"
    ]
    
    company_names = [
        "Technologies", "Solutions", "Systems", "Industries", "Enterprises", "Services", "Associates", "Consultants",
        "Properties", "Products", "Resources", "Holdings", "Management", "Communications", "Logistics", "Networks",
        "Innovations", "International", "Development", "Investments"
    ]
    
    company_types = [
        "LLC", "Inc.", "Corporation", "Corp.", "Associates", "Partners", "Group", "Foundation", "Company", "Co."
    ]
    
    # 65% chance of person, 35% chance of company
    if random.random() < 0.65:
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    else:
        company_name_type = random.randint(1, 3)
        if company_name_type == 1:
            # e.g. "Johnson Industries Inc."
            return f"{random.choice(last_names)} {random.choice(company_names)} {random.choice(company_types)}"
        elif company_name_type == 2:
            # e.g. "Advanced Digital Solutions LLC"
            return f"{random.choice(company_prefixes)} {random.choice(company_names)} {random.choice(company_types)}"
        else:
            # Made-up company name with tech-sounding syllables, e.g. "NexTech Corp."
            syllables = ["Ad", "Tech", "Med", "Net", "Eco", "Bio", "Sol", "Ven", "Dyn", "Qua", "Cre", "Pro", 
                      "Con", "Nex", "Opt", "Max", "Zen", "Viv", "Syn", "Tri"]
            
            name_length = random.randint(2, 3)
            company_name = "".join(random.sample(syllables, name_length))
            return f"{company_name} {random.choice(company_types)}"

def generate_phone():
    formats = [
        "({area}) {prefix}-{line}",
        "{area}-{prefix}-{line}",
        "{area}.{prefix}.{line}"
    ]
    
    area_code = random.randint(201, 989)  # Valid US area codes
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    
    chosen_format = random.choice(formats)
    return chosen_format.format(area=area_code, prefix=prefix, line=line)

def generate_street_number():
    return str(random.randint(1, 9999))

def generate_street_name():
    street_names = [
        "Main", "Oak", "Pine", "Maple", "Cedar", "Elm", "Washington", "Park", "Lake", "Hill",
        "River", "View", "Ridge", "Forest", "High", "Meadow", "Valley", "Spring", "Sunset", "Sunrise",
        "Market", "Church", "Mill", "Bridge", "First", "Second", "Third", "Fourth", "Fifth", "Sixth",
        "Highland", "Lincoln", "Jackson", "Franklin", "Adams", "Jefferson", "Madison", "Wilson", "Monroe", "Grant",
        "Central", "Broadway", "Railroad", "Water", "College", "Columbia", "Pearl", "Walnut", "Chestnut", "Cherry"
    ]
    return random.choice(street_names)

def generate_street_type():
    street_types = [
        "St.", "St", "Street", "Ave.", "Ave", "Avenue", "Blvd.", "Blvd", "Boulevard", "Rd.", "Rd", "Road",
        "Ln.", "Ln", "Lane", "Dr.", "Dr", "Drive", "Way", "Place", "Pl.", "Ct.", "Ct", "Court"
    ]
    return random.choice(street_types)

def generate_location():
    location_types = random.randint(1, 4)
    
    if location_types == 1:  # Street address
        return f"{generate_street_number()} {generate_street_name()} {generate_street_type()}"
    elif location_types == 2:  # Apartment
        apt_prefixes = ["Apt", "Apartment", "Unit", "Suite", "#"]
        apt_number = random.randint(1, 9999)
        return f"{apt_prefixes[random.randint(0, len(apt_prefixes)-1)]} #{apt_number}, {generate_street_number()} {generate_street_name()} {generate_street_type()}"
    elif location_types == 3:  # P.O. Box
        box_number = random.randint(1, 9999)
        return f"P.O. Box {box_number}, {random.randint(1000, 9999)} {generate_street_name()} {generate_street_type()}"
    else:  # Building/complex
        building_types = ["Tower", "Plaza", "Building", "Center", "Complex", "Village", "Commons", "Park", "Square", "Place"]
        building_name = f"{generate_street_name()} {random.choice(building_types)}"
        return f"{building_name}, {generate_street_number()} {generate_street_name()} {generate_street_type()}"

def generate_city():
    cities = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego",
        "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "Indianapolis",
        "San Francisco", "Seattle", "Denver", "Washington DC", "Boston", "El Paso", "Nashville", "Detroit",
        "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore", "Milwaukee", "Albuquerque",
        "Tucson", "Fresno", "Sacramento", "Kansas City", "Long Beach", "Mesa", "Atlanta", "Colorado Springs",
        "Raleigh", "Omaha", "Miami", "Oakland", "Minneapolis", "Tulsa", "Wichita", "New Orleans", "Arlington",
        "Cleveland", "Bakersfield", "Tampa", "Aurora", "Honolulu", "Anaheim", "Santa Ana", "Corpus Christi",
        "Riverside", "St. Louis", "Lexington", "Pittsburgh", "Anchorage", "Stockton", "Cincinnati", "St. Paul"
    ]
    return random.choice(cities)

def generate_date():
    # Generate a date within the last 10 years
    start_date = datetime.now() - timedelta(days=365*10)
    end_date = datetime.now()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    
    # Format as MM-DD-YYYY as requested
    return random_date.strftime("%m-%d-%Y")

def generate_client_data(num_records):
    clients = []
    
    for i in range(1, num_records + 1):
        client = {
            "client_id": generate_client_id(i),
            "client_zipcode": generate_zipcode(),
            "client_name": generate_name(),
            "client_phone": generate_phone(),
            "client_location": generate_location(),
            "client_city": generate_city(),
            "client_datejoined": generate_date()
        }
        clients.append(client)
    
    return clients

def save_to_csv(clients, filename="client_data.csv"):
    fieldnames = ["client_id", "client_zipcode", "client_name", "client_phone", 
                 "client_location", "client_city", "client_datejoined"]
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for client in clients:
            writer.writerow(client)
    print(f"Data saved to {filename}")

def print_sql_insert_statements(clients):
    for client in clients:
        columns = ["client_id", "client_zipcode", "client_name", "client_phone", 
                  "client_location", "client_city", "client_datejoined"]
        
        values = [
            f"'{client['client_id']}'",
            f"'{client['client_zipcode']}'",
            f"'{client['client_name'].replace('\'', '\'\'')}'",
            f"'{client['client_phone']}'",
            f"'{client['client_location'].replace('\'', '\'\'')}'",
            f"'{client['client_city']}'",
            f"'{client['client_datejoined']}'"
        ]
        
        columns_str = ", ".join(columns)
        values_str = ", ".join(values)
        
        sql = f"INSERT INTO client ({columns_str}) VALUES ({values_str});"
        print(sql)

def generate_sql_file(clients, filename="client_inserts.sql"):
    with open(filename, 'w') as sqlfile:
        sqlfile.write("-- SQL Insert statements for client data\n\n")
        
        for client in clients:
            columns = ["client_id", "client_zipcode", "client_name", "client_phone", 
                      "client_location", "client_city", "client_datejoined"]
            
            values = [
                f"'{client['client_id']}'",
                f"'{client['client_zipcode']}'",
                f"'{client['client_name'].replace('\'', '\'\'')}'",
                f"'{client['client_phone']}'",
                f"'{client['client_location'].replace('\'', '\'\'')}'",
                f"'{client['client_city']}'",
                f"'{client['client_datejoined']}'"
            ]
            
            columns_str = ", ".join(columns)
            values_str = ", ".join(values)
            
            sql = f"INSERT INTO client ({columns_str}) VALUES ({values_str});\n"
            sqlfile.write(sql)
    
    print(f"SQL statements saved to {filename}")

if __name__ == "__main__":
    # Number of client records to generate
    num_records = int(input("How many client records do you want to generate? "))
    
    # Generate client data
    clients = generate_client_data(num_records)
    
    # Ask for output format preference
    print("\nSelect output format(s):")
    print("1. CSV file")
    print("2. SQL insert statements in console")
    print("3. SQL insert statements in file")
    print("4. All of the above")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice in ['1', '4']:
        csv_filename = input("Enter CSV filename (default: client_data.csv): ") or "client_data.csv"
        save_to_csv(clients, csv_filename)
    
    if choice in ['2', '4']:
        print("\nSQL Insert Statements:")
        print_sql_insert_statements(clients)
    
    if choice in ['3', '4']:
        sql_filename = input("Enter SQL filename (default: client_inserts.sql): ") or "client_inserts.sql"
        generate_sql_file(clients, sql_filename)
        
    print("\nData generation complete!")