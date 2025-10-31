-- Create Kafka Source Table for Traffic Sensors
CREATE TABLE traffic_sensors (
    sensor_id STRING,
    sensor_type STRING,
    vehicle_count INT,
    average_speed DOUBLE,
    congestion_level STRING,
    location ROW<latitude DOUBLE, longitude DOUBLE>,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'traffic-sensors',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-sql-consumer',
    'scan.startup.mode' = 'latest-offset',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601'
);

-- Detect Anomalies (High Congestion)
CREATE TABLE traffic_anomalies (
    sensor_id STRING,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    avg_vehicle_count DOUBLE,
    avg_speed DOUBLE,
    high_congestion_count BIGINT
) WITH (
    'connector' = 'print'
);

-- Windowed Aggregation and Anomaly Detection
INSERT INTO traffic_anomalies
SELECT 
    sensor_id,
    TUMBLE_START(event_time, INTERVAL '1' MINUTE) as window_start,
    TUMBLE_END(event_time, INTERVAL '1' MINUTE) as window_end,
    AVG(vehicle_count) as avg_vehicle_count,
    AVG(average_speed) as avg_speed,
    COUNT(*) FILTER (WHERE congestion_level = 'high') as high_congestion_count
FROM traffic_sensors
GROUP BY sensor_id, TUMBLE(event_time, INTERVAL '1' MINUTE)
HAVING COUNT(*) FILTER (WHERE congestion_level = 'high') > 0;
