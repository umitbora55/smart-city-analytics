"""
Smart City Analytics REST API
Real-time data access and statistics
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import pyarrow.parquet as pq


app = FastAPI(
    title="Smart City Analytics API",
    description="Real-time IoT sensor data and analytics",
    version="1.0.0",
)


class SensorData(BaseModel):
    sensor_id: str
    sensor_type: str
    timestamp: str
    vehicle_count: Optional[int] = None
    average_speed: Optional[float] = None
    congestion_level: Optional[str] = None


class HealthCheck(BaseModel):
    status: str
    timestamp: str
    services: dict


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Smart City Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    services = {
        "api": "healthy",
        "kafka": check_kafka_health(),
        "spark": "not_implemented",
    }
    
    return {
        "status": "healthy" if all(s == "healthy" for s in services.values() if s != "not_implemented") else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": services
    }


def check_kafka_health() -> str:
    """Check if Kafka is accessible"""
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=['localhost:9092'],
            consumer_timeout_ms=1000
        )
        consumer.close()
        return "healthy"
    except KafkaError:
        return "unhealthy"
    except Exception:
        return "unknown"


@app.get("/api/v1/sensors/latest")
async def get_latest_sensors(limit: int = 10):
    """Get latest sensor data from Kafka"""
    try:
        consumer = KafkaConsumer(
            'traffic-sensors',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='latest',
            consumer_timeout_ms=5000,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        messages = []
        for message in consumer:
            messages.append(message.value)
            if len(messages) >= limit:
                break
        
        consumer.close()
        
        return {
            "count": len(messages),
            "data": messages
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


@app.get("/api/v1/statistics/kafka")
async def get_kafka_statistics():
    """Get Kafka topic statistics"""
    try:
        from kafka.admin import KafkaAdminClient
        
        admin = KafkaAdminClient(
            bootstrap_servers=['localhost:9092'],
            client_id='api-admin'
        )
        
        topics = admin.list_topics()
        
        stats = {
            "topics": list(topics),
            "topic_count": len(topics),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        admin.close()
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/v1/statistics/parquet")
async def get_parquet_statistics():
    """Get Parquet file statistics"""
    try:
        parquet_path = "/mnt/bigdata/spark-data/traffic"
        
        # Read Parquet file
        table = pq.read_table(parquet_path)
        df = table.to_pandas()
        
        stats = {
            "total_records": len(df),
            "columns": list(df.columns),
            "file_path": parquet_path,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add sensor statistics
        if 'sensor_id' in df.columns:
            stats['unique_sensors'] = df['sensor_id'].nunique()
            stats['top_sensors'] = df['sensor_id'].value_counts().head(5).to_dict()
        
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/v1/sensors/{sensor_id}")
async def get_sensor_data(sensor_id: str):
    """Get data for specific sensor from Parquet"""
    try:
        parquet_path = "/mnt/bigdata/spark-data/traffic"
        
        table = pq.read_table(parquet_path)
        df = table.to_pandas()
        
        # Filter by sensor_id
        sensor_df = df[df['sensor_id'] == sensor_id]
        
        if len(sensor_df) == 0:
            raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} not found")
        
        return {
            "sensor_id": sensor_id,
            "record_count": len(sensor_df),
            "data": sensor_df.to_dict('records')[:100]  # Limit to 100 records
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
