# API Documentation

REST API documentation for Smart City Analytics.

## Overview

The API provides real-time access to processed IoT sensor data and analytics.

**Base URL**: `http://localhost:8000/api/v1`

**Authentication**: Will be implemented in Phase 4

## Endpoints

API endpoints will be documented as they are implemented.

### Planned Endpoints

#### Sensor Data
- `GET /sensors` - List all sensors
- `GET /sensors/{sensor_id}` - Get specific sensor details
- `GET /sensors/{sensor_id}/data` - Get sensor readings

#### Analytics
- `GET /analytics/traffic` - Traffic analytics
- `GET /analytics/weather` - Weather analytics
- `GET /analytics/energy` - Energy consumption analytics

#### Real-time Metrics
- `GET /metrics/realtime` - Current system metrics
- `GET /alerts` - Active alerts

## Response Format

All responses will follow this format:
```json
{
  "status": "success",
  "data": {},
  "timestamp": "2025-10-31T10:00:00Z",
  "request_id": "uuid"
}
```

## Error Handling

Error responses will include:
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  },
  "timestamp": "2025-10-31T10:00:00Z",
  "request_id": "uuid"
}
```

---

**Document Status**: Placeholder, will be updated during Phase 4
