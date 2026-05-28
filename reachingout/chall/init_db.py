import random

from db import get_db


conn = get_db()

# Drop table if it exists
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS directory")

# Create table
cur.execute("""
CREATE TABLE directory (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL
)
""")


# Generate fake data

FIRST_NAMES = ["Archie", "Sergio", "Roland", "Teddy", "Gerald", "Gary", "Myron", "Elton", "Desi", "Forester", "Lillian", "Ruby", "Clara", "Vera", "Nellie", "Winifred", "Agatha", "Verity", "Effie", "Philomena", ]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", ]

DEPARTMENTS = ["HR", "Marketing", "IT", "Customer Service", ]

rows = []
for _ in range(10000):
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    row = {
        "first_name": first_name,
        "last_name": last_name,
        "department": random.choice(DEPARTMENTS),
        "email": f"{first_name}.{last_name}@example.com".lower(),
        "phone_number": f"555-{random.randint(100, 999)}-{random.randint(100, 999)}",
    }
    rows.append(row)

# Insert it
cur.executemany("""
INSERT INTO directory (first_name, last_name, department, email, phone_number)
VALUES (%(first_name)s, %(last_name)s, %(department)s, %(email)s, %(phone_number)s)
""", rows)

conn.commit()
