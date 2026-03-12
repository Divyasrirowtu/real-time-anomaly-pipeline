import json
import time
import random
import os
from datetime import datetime
from kafka import KafkaProducer

# Environment variables
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "raw_events")

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

devices = ["device_1", "device_2", "device_3", "device_4"]

print("Producer started... sending events")

while True:
    event = {
        "device_id": random.choice(devices),
        "timestamp": datetime.utcnow().isoformat(),
        "metric": round(random.uniform(20, 100), 2)
    }

    producer.send(TOPIC_NAME, event)

    print(f"Sent event: {event}")

    time.sleep(1)