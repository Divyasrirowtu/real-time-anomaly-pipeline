import json
import os
import psycopg2
from kafka import KafkaConsumer

# Environment variables
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "anomalies")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "anomalies_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)

cursor = conn.cursor()

# Kafka Consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("DB Sink started... saving anomalies to database")

for message in consumer:
    anomaly = message.value

    device_id = anomaly["device_id"]
    timestamp = anomaly["timestamp"]
    metric = anomaly["metric"]
    mean = anomaly["mean"]
    std_dev = anomaly["std_dev"]

    insert_query = """
    INSERT INTO anomalies (device_id, event_timestamp, metric_value, mean_value, std_dev)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (device_id, timestamp, metric, mean, std_dev))
    conn.commit()

    print("Saved anomaly:", anomaly)