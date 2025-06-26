import requests
from tinydb import TinyDB
from datetime import datetime
import time

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
    timestamp = datetime.now().timestamp()

    # Organizes the extracted data into a clean dictionary format    
    transformed_data = {
        'value': value,
        'cryptocurrency': cryptocurrency,
        'currency': currency,
        'timestamp': timestamp
    }
    return transformed_data                            # Returns the transformed (cleaned) data

# Define load function
def load_bitcoin_tinydb(data, db_name='bitcoin_json'):
    db = TinyDB(db_name)         # Creates or opens a TinyDB database file with the given name
    db.insert(data)              # Inserts the provided data into the database
    print('Load done with success')  # Prints confirmation message after loading the data


# Executes only if the script is run directly (not imported as a module)
if __name__ == '__main__':
    while True:
        data = extract_bitcoin_data()                 # Step 1: Extract data from the API
        transformed_data = transform_bitcoin_data(data)  # Step 2: Clean and structure the data
        load_bitcoin_tinydb(transformed_data)         # Step 3: Store the data in the database
        time.sleep(12)                                # Waits 12 seconds before repeating the process
