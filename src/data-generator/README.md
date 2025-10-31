# IoT Data Generator

Simulates IoT sensor data for Smart City Analytics project.

## Features

- Generates realistic traffic, weather, and energy sensor data
- Configurable number of sensors and generation intervals
- Time-based patterns (rush hour, day/night cycles)
- Output to console or file

## Usage
```bash
# Activate virtual environment
source ../../venv/bin/activate

# Run generator
python generator.py
```

## Configuration

Edit `config.yaml` to customize:
- Number of sensors per type
- Data generation interval
- Sensor types to enable/disable
- Location boundaries

## Data Schema

### Traffic Sensor
```json
{
  "sensor_id": "TRAFFIC_0001",
  "sensor_type": "traffic",
  "location": {"latitude": 40.5, "longitude": 28.5},
  "timestamp": "2025-10-31T10:00:00.000000",
  "vehicle_count": 120,
  "average_speed": 35.5,
  "congestion_level": "medium"
}
```

### Weather Sensor
```json
{
  "sensor_id": "WEATHER_0001",
  "sensor_type": "weather",
  "location": {"latitude": 40.5, "longitude": 28.5},
  "timestamp": "2025-10-31T10:00:00.000000",
  "temperature": 22.5,
  "humidity": 65.2,
  "pressure": 1013.2,
  "wind_speed": 12.3
}
```

### Energy Sensor
```json
{
  "sensor_id": "ENERGY_0001",
  "sensor_type": "energy",
  "location": {"latitude": 40.5, "longitude": 28.5},
  "timestamp": "2025-10-31T10:00:00.000000",
  "power_consumption": 3500.5,
  "voltage": 230.2,
  "current": 15.2
}
```
