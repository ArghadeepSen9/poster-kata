import psycopg2
from faker import Faker
import random

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,  # Port for source-db
    database="source",
    user="user",
    password="password"
)
cursor = conn.cursor()

# Faker instance
fake = Faker()

# Create table in source DB
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        poster_content VARCHAR(100),
        quantity INT,
        price DECIMAL,
        email VARCHAR(100),
        sales_rep VARCHAR(100),
        promo_code VARCHAR(20)
    );
""")
conn.commit()

# Populate table with fake data
for _ in range(100):
    poster_content = random.choice(["Millennium Falcon", "X-wing", "TIE Fighter"])
    quantity = random.randint(1, 10)
    price = round(random.uniform(5, 50), 2)
    email = fake.email()
    sales_rep = fake.email(domain="swposters.com")
    promo_code = fake.word()

    cursor.execute("""
        INSERT INTO sales (poster_content, quantity, price, email, sales_rep, promo_code)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (poster_content, quantity, price, email, sales_rep, promo_code))

conn.commit()
cursor.close()
conn.close()

print("Fake data inserted into the source database.")
