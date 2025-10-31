"""
IoT Data Generator V2 - Hybrid Approach
Combines real API data with simulated data
"""
import json
import time
import random
import yaml
from typing import List, Dict
from pathlib import Path
from sensor_models import TrafficSensor, WeatherSensor, EnergySensor
from data_fetcher import HybridDataManager


class HybridIoTDataGenerator:
    """Hybrid data generator using real and simulated data"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize generator with configuration"""
        self.config = self._load_config(config_path)
        self.sensors = self._initialize_sensors()
        self.hybrid_manager = HybridDataManager()
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
        
        # Create weather sensors (fewer, as real API has rate limits)
        if self.config['sensor_types']['weather']['enabled']:
            # Reduce weather sensors to respect API limits
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
        """Generate one batch of data from all sensors (hybrid approach)"""
        batch = []
        
        # Traffic sensors (simulated only for now)
        for sensor in self.sensors['traffic']:
            data = sensor.generate_data()
            batch.append(data)
        
        # Weather sensors (hybrid: real API + simulated)
        for sensor in self.sensors['weather']:
            simulated_data = sensor.generate_data()
            # Try to get real data
            hybrid_data = self.hybrid_manager.get_weather_data(
                sensor.location['latitude'],
                sensor.location['longitude'],
                simulated_data
            )
            batch.append(hybrid_data)
        
        # Energy sensors (simulated only for now)
        for sensor in self.sensors['energy']:
            data = sensor.generate_data()
            batch.append(data)
        
        return batch
    
    def run(self, duration: int = None, output_file: str = None):
        """
        Run the hybrid generator
        
        Args:
            duration: How long to run in seconds (None = infinite)
            output_file: File to save generated data (None = print to console)
        """
        self.running = True
        interval = self.config['general']['data_generation_interval']
        
        start_time = time.time()
        batch_count = 0
        
        print(f"Starting Hybrid IoT Data Generator...")
        print(f"Sensors: {sum(len(s) for s in self.sensors.values())} total")
        print(f"  - Traffic: {len(self.sensors['traffic'])} (simulated)")
        print(f"  - Weather: {len(self.sensors['weather'])} (hybrid)")
        print(f"  - Energy: {len(self.sensors['energy'])} (simulated)")
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
                    # Print sample
                    if batch_count % 10 == 0:  # Print every 10 batches
                        print(f"\nBatch #{batch_count} - {len(batch)} records")
                        for record in batch[:2]:
                            print(json.dumps(record, indent=2))
                
                # Wait for next interval
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
            print(f"Total records: {total_records}")
            print(f"Records/second: {total_records/elapsed:.2f}")
            
            # Print hybrid statistics
            self.hybrid_manager.print_statistics()


if __name__ == "__main__":
    generator = HybridIoTDataGenerator()
    
    # Run for 30 seconds
    generator.run(duration=30)
