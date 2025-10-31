# Architecture Overview

## System Design Philosophy

This project implements a modern data lakehouse architecture combining the best of data lakes and data warehouses. The system is designed for:

- High throughput (1M+ events/second)
- Low latency (<100ms p99)
- Exactly-once processing semantics
- Horizontal scalability
- Fault tolerance

## Architecture Layers

### 1. Data Ingestion Layer
- **Apache Kafka**: Distributed message broker
- **Topics**: Separate topics for traffic, weather, and energy sensors
- **Partitioning Strategy**: Partition by sensor_id for load distribution
- **Replication Factor**: 3 for high availability

### 2. Stream Processing Layer
- **Apache Flink**: Real-time stream processing
- **Processing Guarantees**: Exactly-once semantics
- **State Management**: RocksDB for stateful operations
- **Windowing**: Tumbling and sliding windows for aggregations

### 3. Storage Layer
- **Apache Iceberg**: Table format for data lakehouse
- **MinIO**: S3-compatible object storage
- **Schema Evolution**: Built-in support for schema changes
- **Time Travel**: Query historical data states

### 4. Batch Processing Layer
- **Apache Spark**: Large-scale batch processing
- **Integration**: Direct read from Iceberg tables
- **Optimization**: Predicate pushdown, column pruning

### 5. Orchestration Layer
- **Apache Airflow**: Workflow management
- **DAGs**: Scheduled batch jobs and maintenance tasks
- **Monitoring**: Built-in task monitoring

### 6. API & Visualization Layer
- **REST API**: FastAPI for real-time queries
- **Dashboard**: Grafana for metrics visualization
- **Alerting**: Prometheus AlertManager

## Data Flow

### Real-Time Path (Kappa Architecture)
```
IoT Sensors → Kafka → Flink → Iceberg → API/Dashboard
```

### Batch Path (Lambda Architecture)
```
IoT Sensors → Kafka → Iceberg → Spark → Iceberg → API/Dashboard
```

## Technology Decisions

### Why Flink over Spark Streaming?
- Lower latency
- True stream processing (not micro-batching)
- Better state management
- Exactly-once semantics out of the box

### Why Iceberg over Delta Lake?
- Better multi-engine support
- Advanced partitioning strategies
- Hidden partitioning
- Time travel capabilities

### Why MinIO?
- S3-compatible API
- Can run locally for development
- Easy migration to cloud object storage

## Scalability Considerations

- **Horizontal Scaling**: All components designed to scale out
- **Partitioning**: Strategic partitioning for parallel processing
- **Caching**: Redis for frequently accessed data
- **Load Balancing**: Nginx for API layer

## Security

- Network isolation with Docker networks
- Authentication for all services
- Encryption in transit (TLS)
- Secret management with environment variables

## Monitoring Strategy

- **Metrics Collection**: Prometheus exporters for all services
- **Visualization**: Grafana dashboards
- **Alerting**: Rule-based alerts for anomalies
- **Logging**: Centralized logging with ELK stack (future)

---

**Document Status**: Living document, updated as architecture evolves
