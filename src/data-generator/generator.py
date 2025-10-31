"""
IoT Data Generator - Main Module
Generates simulated sensor data for traffic, weather, and energy sensors
"""
import json
import time
import random
import yaml
from typing import List, Dict
from pathlib import Path
from sensor_models import TrafficSensor, WeatherSensor, EnergySensor


class IoTDataGenerator:
    """Main data generator class"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize generator with configuration"""
        self.config = self._load_config(config_path)
        self.sensors = self._initialize_sensors()
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
            for i in range(sensors_per_type):
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
        
        for sensor_type, sensor_list in self.sensors.items():
            for sensor in sensor_list:
                data = sensor.generate_data()
                batch.append(data)
        
        return batch
    
    def run(self, duration: int = None, output_file: str = None):
        """
        Run the generator
        
        Args:
            duration: How long to run in seconds (None = infinite)
            output_file: File to save generated data (None = print to console)
        """
        self.running = True
        interval = self.config['general']['data_generation_interval']
        
        start_time = time.time()
        batch_count = 0
        
        print(f"Starting IoT Data Generator...")
        print(f"Sensors: {sum(len(s) for s in self.sensors.values())} total")
        print(f"Interval: {interval} seconds")
        print("-" * 50)
        
        try:
            while self.running:
                # Check duration
                if duration and (time.time() - start_time) >= duration:
                    break
                
                # Generate batch
                batch = self.generate_batch()
                batch_count += 1
                
                # Output data
                if output_file:
                    with open(output_file, 'a') as f:
                        for record in batch:
                            f.write(json.dumps(record) + '\n')
                else:
                    # Print sample (only first 3 records)
                    print(f"\nBatch #{batch_count} - {len(batch)} records")
                    for record in batch[:3]:
                        print(json.dumps(record, indent=2))
                    if len(batch) > 3:
                        print(f"... and {len(batch) - 3} more records")
                
                # Wait for next interval
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nGenerator stopped by user")
        finally:
            self.running = False
            elapsed = time.time() - start_time
            total_records = batch_count * sum(len(s) for s in self.sensors.values())
            print(f"\nSummary:")
            print(f"Runtime: {elapsed:.2f} seconds")
            print(f"Batches: {batch_count}")
            print(f"Total records: {total_records}")
            print(f"Records/second: {total_records/elapsed:.2f}")


if __name__ == "__main__":
    generator = IoTDataGenerator()
    
    # Run for 30 seconds, printing to console
    generator.run(duration=30)
