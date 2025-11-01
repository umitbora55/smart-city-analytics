# Smart City Analytics REST API

FastAPI-based REST API for accessing IoT sensor data and analytics.

## Features

- Real-time sensor data from Kafka
- Historical data from Parquet files
- Health checks
- Statistics and aggregations
- Auto-generated documentation (Swagger UI)

## Running
```bash
# Activate venv
source ../../venv/bin/activate

# Run API server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Swagger UI
- `GET /api/v1/sensors/latest` - Latest sensor data
- `GET /api/v1/sensors/{sensor_id}` - Specific sensor data
- `GET /api/v1/statistics/kafka` - Kafka statistics
- `GET /api/v1/statistics/parquet` - Parquet statistics

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
