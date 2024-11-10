import requests
import psycopg2

# Set up API URL for starships
SWAPI_URL = "https://swapi.dev/api/starships/"

# Connect to source and dw databases
conn_source = psycopg2.connect(
    host="localhost",
    port=5432,
    database="source",
    user="user",
    password="password"
)
conn_dw = psycopg2.connect(
    host="localhost",
    port=5433,  # Port for dw-db
    database="dw",
    user="user",
    password="password"
)

# Fetch starship data from SWAPI API
def fetch_starship_data():
    starships = []
    response = requests.get(SWAPI_URL)
    while response:
        data = response.json()
        starships.extend(data['results'])
        if data['next']:
            response = requests.get(data['next'])
        else:
            break
    return starships

# Transform and load data into the dw database
def etl_process():
    starships = fetch_starship_data()
    cursor_source = conn_source.cursor()
    cursor_dw = conn_dw.cursor()

    cursor_dw.execute("""
        CREATE TABLE IF NOT EXISTS starship_sales (
            id SERIAL PRIMARY KEY,
            poster_content VARCHAR(100),
            quantity INT,
            price DECIMAL,
            sales_rep VARCHAR(100),
            promo_code VARCHAR(20),
            film_name VARCHAR(100),
            film_year INT
        );
    """)
    conn_dw.commit()

    # Join data from source DB with starship data
    for ship in starships:
        cursor_source.execute("SELECT poster_content, quantity, price, sales_rep, promo_code FROM sales WHERE poster_content = %s;", (ship['name'],))
        for (poster_content, quantity, price, sales_rep, promo_code) in cursor_source.fetchall():
            for film in ship['films']:
                film_data = requests.get(film).json()
                film_name = film_data['title']
                film_year = int(film_data['release_date'][:4])

                cursor_dw.execute("""
                    INSERT INTO starship_sales (poster_content, quantity, price, sales_rep, promo_code, film_name, film_year)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (poster_content, quantity, price, sales_rep, promo_code, film_name, film_year))
    conn_dw.commit()
    cursor_source.close()
    cursor_dw.close()
    conn_source.close()
    conn_dw.close()
    print("ETL process completed.")

if __name__ == "__main__":
    etl_process()
