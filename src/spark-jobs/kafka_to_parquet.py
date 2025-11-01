"""
Spark Batch Job - Kafka to Parquet
Reads data from Kafka and writes to Parquet files
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, count, max as spark_max
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
import time


def create_spark_session():
    """Create Spark session with Kafka support"""
    spark = SparkSession.builder \
        .appName("KafkaToParquet") \
        .master("spark://localhost:7077") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark


def define_schema():
    """Define schema for traffic sensor data"""
    return StructType([
        StructField("sensor_id", StringType(), True),
        StructField("sensor_type", StringType(), True),
        StructField("vehicle_count", IntegerType(), True),
        StructField("average_speed", DoubleType(), True),
        StructField("congestion_level", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("location", StructType([
            StructField("latitude", DoubleType(), True),
            StructField("longitude", DoubleType(), True)
        ]), True)
    ])


def read_from_kafka(spark, topic="traffic-sensors"):
    """Read data from Kafka topic"""
    print(f"Reading from Kafka topic: {topic}")
    
    df = spark.read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .option("endingOffsets", "latest") \
        .load()
    
    return df


def process_data(df, schema):
    """Process Kafka data"""
    # Parse JSON
    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Show sample
    print("\nSample data:")
    parsed_df.show(5, truncate=False)
    
    # Basic statistics
    print("\nData Statistics:")
    print(f"Total records: {parsed_df.count()}")
    
    # Aggregations
    if "vehicle_count" in parsed_df.columns and "average_speed" in parsed_df.columns:
        agg_df = parsed_df.groupBy("sensor_id") \
            .agg(
                count("*").alias("total_records"),
                avg("vehicle_count").alias("avg_vehicles"),
                avg("average_speed").alias("avg_speed"),
                spark_max("vehicle_count").alias("max_vehicles")
            )
        
        print("\nAggregated Statistics by Sensor:")
        agg_df.show(10)
    
    return parsed_df


def write_to_parquet(df, output_path="/mnt/bigdata/spark-data/traffic"):
    """Write data to Parquet format"""
    print(f"\nWriting to Parquet: {output_path}")
    
    df.write \
        .mode("overwrite") \
        .parquet(output_path)
    
    print(f"Successfully written to {output_path}")


def main():
    """Main execution"""
    print("="*70)
    print("Spark Batch Job: Kafka to Parquet")
    print("="*70)
    
    # Create Spark session
    spark = create_spark_session()
    
    # Define schema
    schema = define_schema()
    
    # Read from Kafka
    kafka_df = read_from_kafka(spark, "traffic-sensors")
    
    # Process data
    processed_df = process_data(kafka_df, schema)
    
    # Write to Parquet
    write_to_parquet(processed_df)
    
    print("\n" + "="*70)
    print("Job completed successfully!")
    print("="*70)
    
    spark.stop()


if __name__ == "__main__":
    main()
