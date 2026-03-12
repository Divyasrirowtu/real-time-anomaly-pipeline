import json
import os
import statistics
from collections import deque, defaultdict
from kafka import KafkaConsumer, KafkaProducer
import time

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
INPUT_TOPIC = os.getenv("INPUT_TOPIC", "raw_events")
OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC", "anomalies")

# Retry connection to Kafka
while True:
    try:
        consumer = KafkaConsumer(
            INPUT_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True
        )
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        break
    except Exception as e:
        print(f"Kafka connection failed: {e}, retrying in 5 seconds...")
        time.sleep(5)

device_windows = defaultdict(lambda: deque(maxlen=100))
print("Consumer started with error handling...")

for message in consumer:
    try:
        event = message.value
        device_id = event.get("device_id")
        metric = event.get("metric")

        if device_id is None or metric is None:
            print("Malformed message skipped:", event)
            continue

        window = device_windows[device_id]
        window.append(metric)

        if len(window) < 10:
            continue

        mean_val = statistics.mean(window)
        std_dev = statistics.stdev(window)

        if std_dev == 0:
            continue

        if metric > mean_val + 3 * std_dev or metric < mean_val - 3 * std_dev:
            anomaly_event = {
                "device_id": device_id,
                "timestamp": event["timestamp"],
                "metric": metric,
                "mean": mean_val,
                "std_dev": std_dev
            }
            producer.send(OUTPUT_TOPIC, anomaly_event)
            print("Anomaly detected:", anomaly_event)

    except json.JSONDecodeError as e:
        print("JSON parse error, skipping message:", e)
    except Exception as e:
        print("Unexpected error:", e)