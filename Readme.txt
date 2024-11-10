Step 1: Create the two PostgreSQL containers using docker-compose.yml. The containers are: source-db and dw-db
Step 2: Run it using the following command to start the conatiners: docker-compose up -d
Step 3: Install the python package using: pip install psycopg2 faker requests
Step 4: Create the fake data using the script populate_source.py by running the python script: python populate_source.py
Step 5: Run the ETL process with the code present in etl_process.py using the command: python etl_process.py. This creates the starship_sales table in the database: dw
Stpe 6: 
