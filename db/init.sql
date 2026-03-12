CREATE TABLE IF NOT EXISTS anomalies (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    metric_value FLOAT NOT NULL,
    mean_value FLOAT NOT NULL,
    std_dev FLOAT NOT NULL,
    processed_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);