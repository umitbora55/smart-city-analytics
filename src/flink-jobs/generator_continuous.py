"""
Continuous IoT Data Generator - Runs indefinitely
"""
import sys
sys.path.append('../kafka-setup')

from generator_kafka import KafkaIoTDataGenerator

if __name__ == "__main__":
    generator = KafkaIoTDataGenerator()
    
    # Run without duration (infinite)
    print("Starting continuous generator (CTRL+C to stop)...")
    generator.run(duration=None)
