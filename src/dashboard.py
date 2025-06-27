import streamlit as st
from streamlit_autorefresh import st_autorefresh
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to Postgres
def get_latest_prices():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    # Gets the two most recent records
    cur.execute("SELECT value, currency, timestamp FROM bitcoin_table ORDER BY id DESC LIMIT 2;")
    results = cur.fetchall()
    conn.close()
    return results

# Get the data
results = get_latest_prices()
latest = results[0]     # Most recent record
previous = results[1]   # Previous record

# Extract fields and convert Decimal to float
value = float(latest[0])
currency = latest[1]
timestamp = latest[2]

# Calculate the price difference (delta)
delta = value - float(previous[0])

# This will rerun the app every 16000 milliseconds (16 seconds)
st_autorefresh(interval=16000, limit=None, key="datarefresh")

st.title("📈 Bitcoin Price Tracker")

# Display the current price with the variation
st.metric(
    label=f"Bitcoin price ({currency})",
    value=f"${value:,.2f}",
    delta=f"${delta:,.2f}"
)

# Show the last updated timestamp in a cleaner format
st.write(f"Last updated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")