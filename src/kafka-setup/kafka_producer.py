"""
Kafka Producer for IoT sensor data
Sends data to appropriate Kafka topics based on sensor type
"""
import json
import time
from typing import Dict, List
from kafka import KafkaProducer
from kafka.errors import KafkaError


class IoTKafkaProducer:
    """Kafka producer for IoT sensor data"""
    
    def __init__(self, bootstrap_servers: List[str] = ['localhost:9092']):
        """Initialize Kafka producer"""
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',
            retries=3,
            max_in_flight_requests_per_connection=1,
            compression_type='gzip',
            batch_size=16384,
            linger_ms=10
        )
        
        # Topic mapping
        self.topic_mapping = {
            'traffic': 'traffic-sensors',
            'weather': 'weather-sensors',
            'energy': 'energy-sensors'
        }
        
        # Statistics
        self.stats = {
            'sent': 0,
            'failed': 0,
            'by_topic': {}
        }
        
        print("Kafka Producer initialized")
        print(f"Connected to: {bootstrap_servers}")
    
    def send_record(self, record: Dict) -> bool:
        """Send a single record to appropriate Kafka topic"""
        sensor_type = record.get('sensor_type')
        topic = self.topic_mapping.get(sensor_type)
        
        if not topic:
            print(f"Unknown sensor type: {sensor_type}")
            return False
        
        try:
            key = record.get('sensor_id')
            future = self.producer.send(topic, key=key, value=record)
            
            self.stats['sent'] += 1
            self.stats['by_topic'][topic] = self.stats['by_topic'].get(topic, 0) + 1
            
            return True
            
        except KafkaError as e:
            print(f"Failed to send record: {e}")
            self.stats['failed'] += 1
            return False
    
    def send_batch(self, records: List[Dict]) -> int:
        """Send a batch of records"""
        success_count = 0
        
        for record in records:
            if self.send_record(record):
                success_count += 1
        
        self.producer.flush()
        return success_count
    
    def print_statistics(self):
        """Print producer statistics"""
        print(f"\nKafka Producer Statistics:")
        print(f"Total sent: {self.stats['sent']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"By topic:")
        for topic, count in self.stats['by_topic'].items():
            print(f"  - {topic}: {count}")
    
    def close(self):
        """Close the producer"""
        self.producer.flush()
        self.producer.close()
        print("Kafka Producer closed")


if __name__ == "__main__":
    producer = IoTKafkaProducer()
    
    test_record = {
        'sensor_id': 'TEST_001',
        'sensor_type': 'traffic',
        'timestamp': '2025-10-31T10:00:00',
        'vehicle_count': 50,
        'average_speed': 45.5
    }
    
    print(f"\nSending test record...")
    success = producer.send_record(test_record)
    
    if success:
        print("Test record sent successfully!")
        producer.print_statistics()
    
    producer.close()
