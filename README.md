# Smart City Analytics - Real-Time IoT Data Pipeline

A production-grade, end-to-end big data pipeline for processing millions of IoT sensor events in real-time. This project demonstrates advanced data engineering concepts including stream processing, distributed computing, and modern data lakehouse architecture.

## Project Overview

This system simulates and processes data from smart city IoT sensors (traffic, weather, energy) using industry-standard big data tools. The architecture implements both Lambda and Kappa patterns for comparison.

### Key Features

- Real-time stream processing with Apache Flink
- Batch processing with Apache Spark
- Modern data lakehouse using Apache Iceberg
- Distributed message streaming with Apache Kafka
- Workflow orchestration with Apache Airflow
- Containerized deployment with Docker and Kubernetes
- Comprehensive monitoring with Prometheus and Grafana

## Architecture
```
IoT Sensors (Simulated)
         |
         v
Apache Kafka (Message Broker)
         |
         +----> Apache Flink (Stream Processing)
         |              |
         |              v
         |      Real-time Analytics & Anomaly Detection
         |
         +----> Apache Iceberg (Data Lake)
                        |
                        v
                Apache Spark (Batch Processing)
                        |
                        v
                Analytics API & Dashboard
```

## Technology Stack

### Data Ingestion & Streaming
- Apache Kafka 3.x
- Apache NiFi (optional)

### Stream Processing
- Apache Flink 1.18+
- Exactly-once semantics implementation

### Batch Processing
- Apache Spark 3.5+
- PySpark for data transformations

### Storage
- Apache Iceberg (Lakehouse)
- MinIO (S3-compatible object storage)

### Orchestration
- Apache Airflow 2.8+

### Monitoring
- Prometheus
- Grafana
- Custom metrics

### Infrastructure
- Docker & Docker Compose
- Kubernetes (K3s)
- Terraform (Infrastructure as Code)

## Project Structure
```
smart-city-analytics/
├── docs/                      # Documentation
│   ├── architecture/          # Architecture diagrams and decisions
│   └── diagrams/              # System diagrams
├── src/                       # Source code
│   ├── data-generator/        # IoT data simulator
│   ├── kafka-setup/           # Kafka configuration
│   ├── flink-jobs/            # Stream processing jobs
│   ├── spark-jobs/            # Batch processing jobs
│   └── api/                   # REST API
├── infrastructure/            # Infrastructure as Code
│   ├── docker/                # Docker configurations
│   └── kubernetes/            # K8s manifests
├── tests/                     # Unit and integration tests
├── monitoring/                # Monitoring configurations
└── .github/                   # CI/CD workflows
```

## Getting Started

### Prerequisites

- Ubuntu 22.04 or later
- Docker 20.10+
- Docker Compose 1.29+
- Python 3.11+
- Java 11 or 21
- At least 16GB RAM
- At least 50GB free disk space

### Installation

Detailed setup instructions will be added as components are implemented.
```bash
# Clone the repository
git clone https://github.com/umitbora55/smart-city-analytics.git
cd smart-city-analytics

# Setup will be documented in docs/setup-guide.md
```

## Development Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [x] Project structure setup
- [x] IoT data generator implementation
- [x] Kafka cluster setup
- [ ] Basic monitoring stack

### Phase 2: Stream Processing (Weeks 3-4)
- [ ] Flink job development
- [ ] Real-time anomaly detection
- [ ] Exactly-once semantics

### Phase 3: Storage & Batch (Weeks 5-6)
- [ ] Iceberg lakehouse setup
- [ ] Spark batch jobs
- [ ] Time-travel queries

### Phase 4: Orchestration & API (Weeks 7-8)
- [ ] Airflow DAGs
- [ ] REST API development
- [ ] Dashboard implementation

### Phase 5: Production Ready (Week 9-10)
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] Performance optimization
- [ ] Complete documentation

## Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [Setup Guide](docs/setup-guide.md)
- [API Documentation](docs/api-documentation.md)
- [Contributing Guide](CONTRIBUTING.md)

## Performance Metrics

Target performance benchmarks:
- Throughput: 1M+ events/second
- Latency: <100ms (p99)
- Data freshness: <5 seconds
- Availability: 99.9%

## Learning Outcomes

This project demonstrates:
- Building distributed data pipelines
- Stream vs. batch processing trade-offs
- Data lakehouse architecture
- Production-grade monitoring
- Infrastructure as Code
- DevOps best practices for data engineering

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Umit Bora
- GitHub: [@umitbora55](https://github.com/umitbora55)
- Email: umitbora94@gmail.com

## Acknowledgments

Built as a portfolio project to demonstrate advanced data engineering skills including:
- Big data processing at scale
- Modern data architecture patterns
- Production-grade system design
- Best practices in data engineering

---

**Status:** Active Development  
**Last Updated:** October 2025
