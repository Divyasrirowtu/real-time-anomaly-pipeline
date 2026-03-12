import json
import os
import psycopg2
from kafka import KafkaConsumer
import time

# Environment variables
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "anomalies")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "anomalies_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")

# Retry PostgreSQL connection
while True:
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()
        break
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}, retrying in 5 seconds...")
        time.sleep(5)

# Kafka Consumer
while True:
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True
        )
        break
    except Exception as e:
        print(f"Kafka connection failed: {e}, retrying in 5 seconds...")
        time.sleep(5)

print("DB Sink started with error handling...")

for message in consumer:
    try:
        anomaly = message.value
        device_id = anomaly.get("device_id")
        timestamp = anomaly.get("timestamp")
        metric = anomaly.get("metric")
        mean = anomaly.get("mean")
        std_dev = anomaly.get("std_dev")

        if None in [device_id, timestamp, metric, mean, std_dev]:
            print("Incomplete anomaly message skipped:", anomaly)
            continue

        insert_query = """
        INSERT INTO anomalies (device_id, event_timestamp, metric_value, mean_value, std_dev)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (device_id, timestamp, metric, mean, std_dev))
        conn.commit()
        print("Saved anomaly:", anomaly)
    except json.JSONDecodeError as e:
        print("JSON parse error:", e)
    except Exception as e:
        print("Unexpected DB error:", e)