"""
IoT Data Generator V3 - Kafka Integration
Generates IoT data and sends to Kafka topics
"""
import sys
import json
import time
import random
import yaml
from typing import List, Dict
from pathlib import Path

# Add kafka-setup to path
sys.path.append('../kafka-setup')

from sensor_models import TrafficSensor, WeatherSensor, EnergySensor
from data_fetcher import HybridDataManager
from kafka_producer import IoTKafkaProducer


class KafkaIoTDataGenerator:
    """IoT data generator with Kafka integration"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize generator with Kafka producer"""
        self.config = self._load_config(config_path)
        self.sensors = self._initialize_sensors()
        self.hybrid_manager = HybridDataManager()
        self.kafka_producer = IoTKafkaProducer()
        self.running = False
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _generate_location(self) -> Dict[str, float]:
        """Generate random location within city bounds"""
        bounds = self.config['location']['bounds']
        return {
            'latitude': round(random.uniform(bounds['lat_min'], bounds['lat_max']), 6),
            'longitude': round(random.uniform(bounds['lon_min'], bounds['lon_max']), 6)
        }
    
    def _initialize_sensors(self) -> Dict[str, List]:
        """Initialize all sensors"""
        sensors = {
            'traffic': [],
            'weather': [],
            'energy': []
        }
        
        sensors_per_type = self.config['general']['sensors_per_type']
        
        # Create traffic sensors
        if self.config['sensor_types']['traffic']['enabled']:
            for i in range(sensors_per_type):
                sensor_id = f"TRAFFIC_{i:04d}"
                location = self._generate_location()
                sensors['traffic'].append(TrafficSensor(sensor_id, location))
        
        # Create weather sensors
        if self.config['sensor_types']['weather']['enabled']:
            weather_sensor_count = min(10, sensors_per_type)
            for i in range(weather_sensor_count):
                sensor_id = f"WEATHER_{i:04d}"
                location = self._generate_location()
                sensors['weather'].append(WeatherSensor(sensor_id, location))
        
        # Create energy sensors
        if self.config['sensor_types']['energy']['enabled']:
            for i in range(sensors_per_type):
                sensor_id = f"ENERGY_{i:04d}"
                location = self._generate_location()
                sensors['energy'].append(EnergySensor(sensor_id, location))
        
        return sensors
    
    def generate_batch(self) -> List[Dict]:
        """Generate one batch of data from all sensors"""
        batch = []
        
        # Traffic sensors
        for sensor in self.sensors['traffic']:
            data = sensor.generate_data()
            batch.append(data)
        
        # Weather sensors (hybrid)
        for sensor in self.sensors['weather']:
            simulated_data = sensor.generate_data()
            hybrid_data = self.hybrid_manager.get_weather_data(
                sensor.location['latitude'],
                sensor.location['longitude'],
                simulated_data
            )
            batch.append(hybrid_data)
        
        # Energy sensors
        for sensor in self.sensors['energy']:
            data = sensor.generate_data()
            batch.append(data)
        
        return batch
    
    def run(self, duration: int = None):
        """
        Run the generator and send data to Kafka
        
        Args:
            duration: How long to run in seconds (None = infinite)
        """
        self.running = True
        interval = self.config['general']['data_generation_interval']
        
        start_time = time.time()
        batch_count = 0
        
        print(f"Starting Kafka IoT Data Generator...")
        print(f"Sensors: {sum(len(s) for s in self.sensors.values())} total")
        print(f"  - Traffic: {len(self.sensors['traffic'])}")
        print(f"  - Weather: {len(self.sensors['weather'])}")
        print(f"  - Energy: {len(self.sensors['energy'])}")
        print(f"Interval: {interval} seconds")
        print(f"Kafka: localhost:9092")
        print("-" * 50)
        
        try:
            while self.running:
                if duration and (time.time() - start_time) >= duration:
                    break
                
                # Generate batch
                batch = self.generate_batch()
                
                # Send to Kafka
                sent_count = self.kafka_producer.send_batch(batch)
                batch_count += 1
                
                # Print progress
                if batch_count % 50 == 0:
                    print(f"Batch #{batch_count} - Sent {sent_count}/{len(batch)} records to Kafka")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nGenerator stopped by user")
        finally:
            self.running = False
            elapsed = time.time() - start_time
            total_records = batch_count * sum(len(s) for s in self.sensors.values())
            
            print(f"\n{'='*50}")
            print(f"Runtime Summary:")
            print(f"{'='*50}")
            print(f"Runtime: {elapsed:.2f} seconds")
            print(f"Batches: {batch_count}")
            print(f"Total records generated: {total_records}")
            print(f"Records/second: {total_records/elapsed:.2f}")
            
            # Statistics
            self.kafka_producer.print_statistics()
            self.hybrid_manager.print_statistics()
            
            # Close connections
            self.kafka_producer.close()


if __name__ == "__main__":
    generator = KafkaIoTDataGenerator()
    
    # Run for 60 seconds
    generator.run(duration=60)
