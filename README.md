# Real-Time Anomaly Detection Pipeline

## Project Overview
This project implements a real-time streaming pipeline that detects anomalies in device event data. It uses Kafka for event streaming, Python services for processing, PostgreSQL for persistence, and Streamlit for real-time visualization.

The system processes live event streams and detects anomalies using a rolling statistical window.

---

## Architecture

Producer → Kafka (raw_events) → Consumer (Anomaly Detection) → Kafka (anomalies) → DB Sink → PostgreSQL → Streamlit Dashboard

---

## Technologies Used

- Apache Kafka
- Zookeeper
- Python
- PostgreSQL
- Streamlit
- Docker
- Docker Compose

---

## Data Flow

1. Producer generates synthetic device events.
2. Events are published to Kafka topic `raw_events`.
3. Consumer reads events and performs anomaly detection.
4. If anomaly detected, event is sent to topic `anomalies`.
5. DB Sink consumes anomalies and stores them in PostgreSQL.
6. Streamlit dashboard displays anomalies in real-time.

---

## Anomaly Detection Logic

For each device:

- Maintain rolling window of last 100 metric values
- Compute Mean and Standard Deviation
- If:

metric > mean + 3 * std_dev  
OR  
metric < mean - 3 * std_dev

Then the event is classified as an anomaly.

---

## Project Structure

real-time-anomaly-pipeline
│
├── docker-compose.yml
├── README.md
│
├── producer
├── consumer
├── db_sink
├── dashboard
└── db


---

## Setup Instructions

### 1. Clone Repository
git clone <repository_url>
cd real-time-anomaly-pipeline


### 2. Start the System
docker-compose up --build


### 3. Open Dashboard

Open browser:
http://localhost:8501


---

## Database Schema

Table: anomalies

| Column | Description |
|------|-------------|
| device_id | Device identifier |
| event_timestamp | Event timestamp |
| metric_value | Recorded metric |
| mean_value | Mean of rolling window |
| std_dev | Standard deviation |
| processed_time | Time anomaly processed |

---

## Verification

Check logs for:

Producer sending events  
Consumer detecting anomalies  
DB Sink saving anomalies

To verify database:
docker exec -it anomaly_postgres psql -U admin -d anomalies_db


Then run:
SELECT * FROM anomalies;


---

## Expected Outcome

- Continuous event generation
- Real-time anomaly detection
- Persistent anomaly storage
- Live updating dashboard

---

## Demo Video

Record a 2–4 minute video showing:

1. Running `docker-compose up`
2. Producer logs
3. Consumer detecting anomalies
4. PostgreSQL query results
5. Live Streamlit dashboard updates

---

## Future Improvements

- Add alert notifications
- Use real IoT data sources
- Deploy on Kubernetes
- Add Grafana monitoring