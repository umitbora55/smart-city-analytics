# Spark Batch Processing Jobs

PySpark jobs for batch processing IoT sensor data.

## Jobs

### kafka_to_parquet.py
Reads all data from Kafka topics and writes to Parquet format.

**Features:**
- Reads from Kafka (earliest to latest offsets)
- Parses JSON data
- Computes aggregations by sensor
- Writes to Parquet format
- Spark UI: http://localhost:8083

## Running Jobs
```bash
# Activate venv
source ../../venv/bin/activate

# Run job
python kafka_to_parquet.py
```

## Output

Parquet files will be written to:
- `/mnt/bigdata/spark-data/traffic/`
