import streamlit as st
import psycopg2
import pandas as pd
import os
import time

# Environment variables
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "anomalies_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")

# Page title
st.title("Real-Time Anomaly Detection Dashboard")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)

query = """
SELECT device_id, event_timestamp, metric_value, mean_value, std_dev, processed_time
FROM anomalies
ORDER BY processed_time DESC
LIMIT 50
"""

# Auto refresh every 10 seconds
placeholder = st.empty()

while True:
    df = pd.read_sql(query, conn)

    with placeholder.container():
        st.subheader("Latest Detected Anomalies")
        st.dataframe(df)

    time.sleep(10)