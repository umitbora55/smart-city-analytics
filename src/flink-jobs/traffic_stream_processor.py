"""
Real-time Stream Processor - Traffic Anomaly Detection
Simulates Flink-style stream processing with Kafka Consumer
"""
import json
import logging
from datetime import datetime
from collections import defaultdict
from kafka import KafkaConsumer
from typing import Dict, List


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TrafficStreamProcessor:
    """
    Real-time traffic stream processor
    Implements windowing, aggregation, and anomaly detection
    """
    
    def __init__(self, bootstrap_servers: List[str] = ['localhost:9092']):
        """Initialize stream processor"""
        self.consumer = KafkaConsumer(
            'traffic-sensors',
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='stream-processor-group',
            consumer_timeout_ms=1000
        )
        
        # Windowed statistics (sensor_id -> metrics)
        self.window_stats = defaultdict(lambda: {
            'count': 0,
            'total_speed': 0,
            'total_vehicles': 0,
            'congestion_high_count': 0
        })
        
        self.window_size = 100  # Process every 100 messages
        self.message_count = 0
        
        # Anomaly statistics
        self.anomaly_stats = {
            'severe_congestion': 0,
            'high_volume': 0,
            'speed_anomaly': 0,
            'total_processed': 0
        }
        
        logger.info("Stream Processor initialized")
        logger.info(f"Subscribed to: traffic-sensors")
    
    def detect_anomaly(self, record: Dict) -> Dict:
        """
        Detect traffic anomalies
        Returns anomaly dict if detected, None otherwise
        """
        anomalies = []
        
        # 1. Severe Congestion: High congestion + Very low speed
        if (record.get('congestion_level') == 'high' and 
            record.get('average_speed', 100) < 25):
            anomalies.append({
                'type': 'severe_congestion',
                'severity': 'high',
                'reason': f"Speed {record['average_speed']} km/h with high congestion"
            })
            self.anomaly_stats['severe_congestion'] += 1
        
        # 2. High Traffic Volume
        if record.get('vehicle_count', 0) > 120:
            anomalies.append({
                'type': 'high_volume',
                'severity': 'medium',
                'reason': f"{record['vehicle_count']} vehicles detected"
            })
            self.anomaly_stats['high_volume'] += 1
        
        # 3. Speed Anomaly: Very slow or very fast
        speed = record.get('average_speed', 50)
        if speed < 15 or speed > 120:
            anomalies.append({
                'type': 'speed_anomaly',
                'severity': 'medium',
                'reason': f"Unusual speed: {speed} km/h"
            })
            self.anomaly_stats['speed_anomaly'] += 1
        
        if anomalies:
            return {
                'sensor_id': record.get('sensor_id'),
                'timestamp': record.get('timestamp'),
                'location': record.get('location'),
                'metrics': {
                    'vehicle_count': record.get('vehicle_count'),
                    'average_speed': record.get('average_speed'),
                    'congestion_level': record.get('congestion_level')
                },
                'anomalies': anomalies
            }
        
        return None
    
    def update_window_stats(self, record: Dict):
        """Update windowed statistics"""
        sensor_id = record.get('sensor_id')
        stats = self.window_stats[sensor_id]
        
        stats['count'] += 1
        stats['total_speed'] += record.get('average_speed', 0)
        stats['total_vehicles'] += record.get('vehicle_count', 0)
        
        if record.get('congestion_level') == 'high':
            stats['congestion_high_count'] += 1
    
    def print_window_summary(self):
        """Print aggregated statistics for the window"""
        print(f"\n{'='*70}")
        print(f"WINDOW SUMMARY - Processed {self.message_count} messages")
        print(f"{'='*70}")
        
        # Top 5 busiest sensors
        busiest = sorted(
            self.window_stats.items(),
            key=lambda x: x[1]['total_vehicles'],
            reverse=True
        )[:5]
        
        print("\nTop 5 Busiest Sensors:")
        for sensor_id, stats in busiest:
            avg_speed = stats['total_speed'] / stats['count'] if stats['count'] > 0 else 0
            avg_vehicles = stats['total_vehicles'] / stats['count'] if stats['count'] > 0 else 0
            print(f"  {sensor_id}: {avg_vehicles:.0f} avg vehicles, "
                  f"{avg_speed:.1f} avg speed, "
                  f"{stats['congestion_high_count']} high congestion")
        
        print(f"\nAnomaly Detection Summary:")
        print(f"  Severe Congestion: {self.anomaly_stats['severe_congestion']}")
        print(f"  High Volume: {self.anomaly_stats['high_volume']}")
        print(f"  Speed Anomaly: {self.anomaly_stats['speed_anomaly']}")
        print(f"  Total Processed: {self.anomaly_stats['total_processed']}")
        print(f"{'='*70}\n")
        
        # Reset window
        self.window_stats.clear()
    
    def run(self):
        """Run the stream processor"""
        logger.info("Starting stream processing...")
        logger.info("Waiting for messages from Kafka...")
        
        try:
            for message in self.consumer:
                record = message.value
                self.message_count += 1
                self.anomaly_stats['total_processed'] += 1
                
                # Update windowed statistics
                self.update_window_stats(record)
                
                # Detect anomalies
                anomaly = self.detect_anomaly(record)
                
                if anomaly:
                    print(f"\n⚠️  ANOMALY DETECTED:")
                    print(f"   Sensor: {anomaly['sensor_id']}")
                    print(f"   Time: {anomaly['timestamp']}")
                    print(f"   Location: {anomaly['location']}")
                    print(f"   Metrics: {anomaly['metrics']}")
                    for anom in anomaly['anomalies']:
                        print(f"   - [{anom['severity'].upper()}] {anom['type']}: {anom['reason']}")
                
                # Print window summary every N messages
                if self.message_count % self.window_size == 0:
                    self.print_window_summary()
                
        except KeyboardInterrupt:
            logger.info("\nStream processor stopped by user")
        finally:
            self.consumer.close()
            logger.info("Consumer closed")


if __name__ == "__main__":
    processor = TrafficStreamProcessor()
    processor.run()
