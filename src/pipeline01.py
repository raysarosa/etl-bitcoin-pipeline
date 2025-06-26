import requests
import psycopg2
import os
from dotenv import load_dotenv
from tinydb import TinyDB
from datetime import datetime
import time

# Load the settings from the .env file
load_dotenv()

# Define a function to extract the data from the API
def extract_bitcoin_data():
    url = 'https://api.coinbase.com/v2/prices/spot'  # API endpoint for Bitcoin spot price
    response = requests.get(url)                     # Sends a GET request to the Coinbase API
    data = response.json()                           # Converts the API response from JSON string to Python dictionary
    return data                                      # Returns the raw data

# Define a function to transform the data
def transform_bitcoin_data(data):
    # Extracts specific fields from the JSON structure
    value = data['data']['amount']
    cryptocurrency = data['data']['base']
    currency = data['data']['currency']
    timestamp = datetime.now()

    # Organizes the extracted data into a clean dictionary format    
    transformed_data = {
        'value': value,
        'cryptocurrency': cryptocurrency,
        'currency': currency,
        'timestamp': timestamp
    }
    return transformed_data                            # Returns the transformed (cleaned) data

# # Define function to load data to Tiny Database
# def load_bitcoin_tinydb(data, db_name='bitcoin_json'):
#     db = TinyDB(db_name)         # Creates or opens a TinyDB database file with the given name
#     db.insert(data)              # Inserts the provided data into the database
#     print('Load done with success')  # Prints confirmation message after loading the data

# Create table in the database (this should be executed only once)
def create_table():
    try:
        # Establish a connection to the PostgreSQL database using environment variables
        conn = psycopg2.connect(
            dbname = os.getenv('DB_NAME'),         # Database name
            user = os.getenv('DB_USER'),           # Database user
            password = os.getenv('DB_PASSWORD'),   # Database password
            host = os.getenv('DB_HOST'),           # Host address
            port = os.getenv('DB_PORT')            # Port number
        )

        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Drop the existing table if it exists
            cur.execute('DROP TABLE IF EXISTS bitcoin_table')

            # Create the table if it does not already exist
            cur.execute('''
                CREATE TABLE IF NOT EXISTS bitcoin_table (
                    id SERIAL PRIMARY KEY,                    -- Auto-incrementing ID
                    value NUMERIC NOT NULL,                   -- Bitcoin price
                    cryptocurrency VARCHAR(10) NOT NULL,      -- e.g., BTC
                    currency VARCHAR(10) NOT NULL,            -- e.g., USD
                    timestamp TIMESTAMP NOT NULL              -- Date and time of the record
                )
                ''')
            conn.commit()  # Save the changes
            print('Table created/verified successfully!')
    
    # Handle and display any errors that occur during the process
    except Exception as e:
        print(f'Error creating table: {e}')
    
    # Always close the connection, even if there was an error
    finally:
        if conn:
            conn.close()



# After creating the database, we define a function to load data into PostgreSQL
def load_bitcoin_postgres(data):
    try:
        # Establish a connection to the PostgreSQL database using environment variables
        conn = psycopg2.connect(
            dbname = os.getenv('DB_NAME'),         # Database name from .env
            user = os.getenv('DB_USER'),           # Username from .env
            password = os.getenv('DB_PASSWORD'),   # Password from .env
            host = os.getenv('DB_HOST'),           # Host address (e.g., localhost)
            port = os.getenv('DB_PORT')            # Port number (usually 5432 for PostgreSQL)
        )
        
        # Open a cursor to execute SQL commands
        with conn.cursor() as cur:
            # Insert data into the bitcoin_table
            cur.execute('''
                INSERT INTO bitcoin_table (value, cryptocurrency, currency, timestamp)
                VALUES (%s, %s, %s, %s)
            ''', (
                data['value'],              # Bitcoin price
                data['cryptocurrency'],     # Cryptocurrency name (e.g., BTC)
                data['currency'],           # Currency (e.g., USD)
                data['timestamp']           # Timestamp of data capture
            ))
            conn.commit()                   # Commit the transaction to the database
            print('Load done successfully!') # Success message
    
    # If there's an error, print it
    except Exception as e:
        print(f'Error loading data: {e}')
    
    # Always close the database connection
    finally:
        if conn:
            conn.close()


# Executes only if the script is run directly (not imported as a module)
if __name__ == '__main__':
    # Table criation to startup
    create_table()
    
    # Main loop
    try:
        while True:
            data = extract_bitcoin_data()                 # Step 1: Extract data from the API
            transformed_data = transform_bitcoin_data(data)  # Step 2: Clean and structure the data
            load_bitcoin_postgres(transformed_data)         # Step 3: Store the data in the database
            time.sleep(12)                              # Waits 12 seconds before repeating the process
    
    except KeyboardInterrupt:
        print('Execution was interrupted by the user')
