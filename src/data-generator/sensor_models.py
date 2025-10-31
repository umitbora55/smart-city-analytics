"""
Sensor data models for IoT simulation
"""
import random
import uuid
from datetime import datetime
from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class SensorBase:
    """Base class for all sensors"""
    sensor_id: str
    sensor_type: str
    location: Dict[str, float]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert sensor data to dictionary"""
        return asdict(self)


class TrafficSensor(SensorBase):
    """Traffic sensor model"""
    
    def __init__(self, sensor_id: str, location: Dict[str, float]):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type="traffic",
            location=location,
            timestamp=datetime.utcnow().isoformat()
        )
        self.vehicle_count = 0
        self.average_speed = 0.0
        self.congestion_level = "low"
    
    def generate_data(self) -> Dict[str, Any]:
        """Generate realistic traffic data"""
        hour = datetime.now().hour
        
        # Simulate rush hour patterns
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            base_count = random.randint(80, 150)
            base_speed = random.uniform(20, 40)
            congestion = random.choice(["medium", "high", "high"])
        else:
            base_count = random.randint(20, 60)
            base_speed = random.uniform(40, 80)
            congestion = random.choice(["low", "low", "medium"])
        
        self.vehicle_count = base_count
        self.average_speed = round(base_speed, 2)
        self.congestion_level = congestion
        self.timestamp = datetime.utcnow().isoformat()
        
        return self.to_dict()


class WeatherSensor(SensorBase):
    """Weather sensor model"""
    
    def __init__(self, sensor_id: str, location: Dict[str, float]):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type="weather",
            location=location,
            timestamp=datetime.utcnow().isoformat()
        )
        self.temperature = 0.0
        self.humidity = 0.0
        self.pressure = 0.0
        self.wind_speed = 0.0
    
    def generate_data(self) -> Dict[str, Any]:
        """Generate realistic weather data"""
        # Base values with small variations
        self.temperature = round(random.uniform(15, 30), 2)
        self.humidity = round(random.uniform(40, 80), 2)
        self.pressure = round(random.uniform(1000, 1025), 2)
        self.wind_speed = round(random.uniform(0, 25), 2)
        self.timestamp = datetime.utcnow().isoformat()
        
        return self.to_dict()


class EnergySensor(SensorBase):
    """Energy consumption sensor model"""
    
    def __init__(self, sensor_id: str, location: Dict[str, float]):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type="energy",
            location=location,
            timestamp=datetime.utcnow().isoformat()
        )
        self.power_consumption = 0.0
        self.voltage = 0.0
        self.current = 0.0
    
    def generate_data(self) -> Dict[str, Any]:
        """Generate realistic energy consumption data"""
        hour = datetime.now().hour
        
        # Simulate daily consumption patterns
        if 6 <= hour <= 22:
            base_power = random.uniform(2000, 5000)
        else:
            base_power = random.uniform(500, 1500)
        
        self.power_consumption = round(base_power, 2)
        self.voltage = round(random.uniform(220, 240), 2)
        self.current = round(self.power_consumption / 230, 2)
        self.timestamp = datetime.utcnow().isoformat()
        
        return self.to_dict()
