#  Real-Time Portfolio Risk Analysis Platform

> **A production-grade financial risk analytics system featuring streaming data ingestion, real-time VaR calculations, REST API, and interactive dashboard**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-2.13--3.8.1-orange.svg)](https://kafka.apache.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5.0-red.svg)](https://spark.apache.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)](https://streamlit.io/)

---

##  **Project Overview**

A comprehensive real-time portfolio risk analysis platform that demonstrates enterprise-grade data engineering and financial analytics capabilities. The system processes streaming market data through a complete pipeline from ingestion to visualization, calculating Value at Risk (VaR) metrics and providing actionable insights for risk management decisions.

### **Key Capabilities**

-  **Real-time streaming** with Apache Kafka (47.8 TPS sustained)
-  **Stream processing** with Apache Spark (5-second windowed aggregations)
-  **AWS Kinesis integration** for cloud-native streaming (5,000+ records)
-  **Value at Risk calculations** at 95% and 99% confidence levels
-  **RESTful API** with FastAPI for programmatic access
-  **Interactive dashboard** with Streamlit for executive insights
-  **Containerized infrastructure** with Docker Compose
-  **Advanced analytics** including concentration risk, diversification, and portfolio optimization

---

##  **Architecture**
```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                                │
│  Market Data Simulator → Generates realistic stock prices       │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STREAMING INGESTION                            │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │  Apache Kafka    │         │  AWS Kinesis     │              │
│  │  - 3 Brokers     │         │  - Cloud Stream  │              │
│  │  - Zookeeper     │         │  - 5000+ records │              │
│  │  - 47.8 TPS      │         │  - boto3 client  │              │
│  └──────────────────┘         └──────────────────┘              │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                 STREAM PROCESSING                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Apache Spark Structured Streaming                       │   │
│  │  - Real-time windowed aggregations (5-second windows)    │   │
│  │  - Sub-5-second latency                                  │   │
│  │  - Exactly-once processing semantics                     │   │
│  │  - Checkpointing for fault tolerance                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RISK ENGINE                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Value at Risk (VaR) Calculator                          │   │
│  │  - Historical simulation method                          │   │
│  │  - 95% and 99% confidence levels                         │   │
│  │  - Portfolio-level aggregation                           │   │
│  │  - Real-time recalculation                               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API LAYER                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  FastAPI REST API                                        │   │
│  │  - GET  /status              → System health             │   │
│  │  - GET  /symbols             → Available symbols         │   │
│  │  - GET  /var/{symbol}        → Symbol-specific VaR       │   │
│  │  - GET  /portfolio/var       → Portfolio-wide VaR        │   │
│  │  - POST /var/calculate       → Custom VaR calculation    │   │
│  │  - WS   /ws/market-data      → Real-time WebSocket       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  VISUALIZATION                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Streamlit Interactive Dashboard                         │   │
│  │  - Executive Dashboard: KPIs, alerts, recommendations    │   │
│  │  - Deep Dive Analysis: Symbol-level risk metrics         │   │
│  │  - Risk Alert System: Real-time monitoring               │   │
│  │  - Portfolio Optimizer: Rebalancing suggestions          │   │
│  │  - Auto-refresh capability (5-second intervals)          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

##  **Quick Start**

### **Prerequisites**

- Python 3.11
- Docker Desktop
- Git

### **1. Clone Repository**
```bash
git clone https://github.com/yourusername/portfolio-risk-analysis.git
cd portfolio-risk-analysis
```

### **2. Set Up Environment**
```bash
# Create conda environment
conda create -n portfolio-risk python=3.11 -y
conda activate portfolio-risk

# Install dependencies
pip install -r requirements.txt
```

### **3. Start Infrastructure**
```bash
# Start Kafka cluster
docker-compose up -d

# Verify services
docker ps
```

### **4. Run the Pipeline**

**Terminal 1 - Market Data Simulator:**
```bash
python src/streaming/kafka_producer.py
```

**Terminal 2 - Spark Streaming:**
```bash
python src/streaming/spark_consumer.py
```

**Terminal 3 - FastAPI Backend:**
```bash
python src/api/main.py
```

**Terminal 4 - Streamlit Dashboard:**
```bash
streamlit run src/dashboard/app.py
```

### **5. Access Applications**

-  **Dashboard:** http://localhost:8501
-  **API Docs:** http://localhost:8000/docs
-  **API Endpoint:** http://localhost:8000/portfolio/var

---

##  **Features & Capabilities**

### **Real-Time Data Streaming**

- **Kafka Producer**: Simulates market data at 47.8 TPS
- **Multi-Symbol Support**: AAPL, GOOGL, MSFT, AMZN, JPM
- **Realistic Price Movements**: Brownian motion simulation
- **High Throughput**: 15,000+ messages processed
- **AWS Kinesis**: Cloud-ready alternative streaming path

### **Stream Processing**

- **Spark Structured Streaming**: 
  - 5-second tumbling windows
  - VWAP (Volume-Weighted Average Price) calculations
  - Price aggregations (min, max, avg)
  - Sub-5-second end-to-end latency
- **Fault Tolerance**: Checkpointing enabled
- **Scalability**: Distributed processing ready

### **Risk Analytics**

#### **Value at Risk (VaR)**
- Historical simulation methodology
- 95% and 99% confidence levels
- Position-level and portfolio-level calculations
- Real-time recalculation on new data

#### **Advanced Metrics**
- **Concentration Risk**: Herfindahl-Hirschman Index (HHI)
- **Diversification Benefit**: Portfolio vs individual VaR comparison
- **Risk Scoring**: 0-100 composite risk score
- **Risk-Adjusted Returns**: Risk % relative to position size

### **REST API (FastAPI)**
```python
# Example API Usage

# Get portfolio VaR
GET http://localhost:8000/portfolio/var
Response: {
  "results": [
    {
      "symbol": "AAPL",
      "var_95": 10.53,
      "var_99": 13.21,
      "current_price": 205.67,
      "num_observations": 100
    }
  ],
  "count": 5,
  "timestamp": "2025-12-27T..."
}

# Calculate custom VaR
POST http://localhost:8000/var/calculate
Body: {
  "symbol": "CUSTOM",
  "prices": [100, 102, 98, 101, 99, ...]
}
```

### **Interactive Dashboard**

#### **1. Executive Dashboard**
- 5 key performance indicators
- Real-time risk alerts (critical/warning/success)
- Interactive Plotly visualizations
- Portfolio composition analysis
- Risk heatmap with treemap visualization
- Downloadable CSV reports

#### **2. Deep Dive Analysis**
- Symbol-level risk gauge
- Confidence level comparisons
- Detailed recommendations per symbol
- Risk classification (Low/Medium/High)

#### **3. Risk Alert System**
- Automated risk threshold monitoring
- High concentration detection
- VaR exceedance alerts
- Actionable recommendations

#### **4. Portfolio Optimizer**
- Target risk score setting
- Rebalancing suggestions
- Risk-adjusted weight recommendations
- Optimization strategy guidance

---

##  **Performance Metrics**

| Metric | Value |
|--------|-------|
| Kafka Throughput | 47.8 TPS sustained |
| Spark Processing Latency | <5 seconds end-to-end |
| API Response Time | <100ms (p95) |
| Dashboard Refresh Rate | 5 seconds (configurable) |
| Total Records Processed | 15,000+ |
| AWS Kinesis Records | 5,168 |
| Concurrent Users Supported | 10+ |

---

##  **Technology Stack**

### **Data Engineering**
- **Apache Kafka**: Distributed streaming platform
- **Apache Spark**: Stream processing engine
- **AWS Kinesis**: Cloud streaming service
- **Docker**: Containerization

### **Backend**
- **FastAPI**: Modern async Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### **Frontend**
- **Streamlit**: Interactive web applications
- **Plotly**: Advanced visualizations
- **Pandas**: Data manipulation

### **DevOps**
- **Docker Compose**: Multi-container orchestration
- **Git**: Version control
- **Conda**: Environment management

---

##  **Project Structure**
```
portfolio-risk-analysis/
├── src/
│   ├── api/                          # FastAPI backend
│   │   ├── __init__.py
│   │   └── main.py                   # API endpoints & logic
│   ├── dashboard/                    # Streamlit frontend
│   │   ├── __init__.py
│   │   └── app.py                    # Interactive dashboard
│   ├── risk_engine/                  # Risk calculations
│   │   ├── __init__.py
│   │   └── simple_var.py             # VaR calculator
│   └── streaming/                    # Data pipeline
│       ├── kafka_producer.py         # Market data generator
│       ├── spark_consumer.py         # Stream processor
│       └── kinesis_producer.py       # AWS Kinesis producer
├── data/
│   ├── processed/                    # Processed datasets
│   └── raw/                          # Raw market data
├── notebooks/                        # Jupyter analysis notebooks
├── docker-compose.yml                # Infrastructure setup
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
└── .gitignore                        # Git ignore rules
```

---

##  **Key Learning Outcomes**

### **Data Engineering**
[X] Real-time data streaming with Apache Kafka  
[X] Stream processing with Apache Spark Structured Streaming  
[X]  AWS cloud services integration (Kinesis)  
[X]  Distributed systems architecture  
[X]  Docker containerization & orchestration  

### **Software Engineering**
[X]  RESTful API design with FastAPI  
[X]  Asynchronous Python programming  
[X]  Production-grade error handling  
[X]  API documentation with OpenAPI/Swagger  
[X]  WebSocket real-time communication  

### **Financial Engineering**
[X]  Value at Risk (VaR) methodology  
[X]  Portfolio risk metrics & analytics  
[X]  Concentration risk measurement (HHI)  
[X]  Diversification benefit calculation  
[X]  Risk-adjusted performance evaluation  

### **Data Visualization**
[X]  Interactive dashboards with Streamlit  
[X]  Advanced charts with Plotly  
[X]  Real-time data refresh patterns  
[X]  Executive-level reporting  
[X]  Actionable insights presentation  

---

##  **Configuration**

### **Kafka Settings**
```yaml
# docker-compose.yml
KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
```

### **Spark Configuration**
```python
# spark_consumer.py
spark = SparkSession.builder \
    .appName("PortfolioRiskAnalysis") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()
```

### **API Settings**
```python
# main.py
API_BASE_URL = "http://localhost:8000"
CORS_ORIGINS = ["*"]  # Configure for production
```

---

##  **Sample Output**

### **VaR Calculation Result**
```json
{
  "symbol": "AAPL",
  "var_95": 10.53,
  "var_99": 13.21,
  "current_price": 205.67,
  "num_observations": 100,
  "timestamp": "2025-12-27T06:30:15.123456"
}
```

### **Risk Alert Example**
```
 HIGH CONCENTRATION RISK
Portfolio is concentrated (HHI: 0.35)
Action: Reduce position sizes in top holdings
```

---

##  **Troubleshooting**

### **Kafka Connection Issues**
```bash
# Check if Kafka is running
docker ps | grep kafka

# Restart Kafka cluster
docker-compose restart

# View Kafka logs
docker logs kafka-broker-1
```

### **Spark Errors**
```bash
# Check Java version
java -version  # Should be Java 11 or 17

# Verify Spark installation
pyspark --version
```

### **API Not Responding**
```bash
# Check if API is running
curl http://localhost:8000/status

# Restart API
python src/api/main.py
```

---

##  **Future Enhancements**

- [ ] Machine learning for VaR prediction
- [ ] Multi-factor risk models
- [ ] Real market data integration (Alpha Vantage, Yahoo Finance)
- [ ] Historical backtesting framework
- [ ] Monte Carlo simulation for scenario analysis
- [ ] Options pricing and Greeks calculation
- [ ] Portfolio optimization algorithms (Mean-Variance, Black-Litterman)
- [ ] Alert notifications (email, Slack, SMS)
- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Performance monitoring with Prometheus/Grafana

---

##  **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

##  **Author**

**Narendranath Edara**  
*Data Engineer | Financial Analytics Enthusiast*

---

##  **Acknowledgments**

- Apache Kafka community for robust streaming platform
- Apache Spark community for powerful processing engine
- FastAPI team for excellent framework
- Streamlit team for intuitive dashboard framework
- Plotly for beautiful visualizations

---

##  **Contact**

For questions, suggestions, or collaboration opportunities:
-  Email: edara.narendranath@gmail.com
-  LinkedIn: [linkedin.com/in/narendranathe](https://www.linkedin.com/in/narendranathe/)
-  GitHub: [github.com/narendranathe](https://github.com/narendranathe)

---

<div align="center">

###  If you find this project useful, please consider giving it a star!

**Built with ❤️ for the Data Engineering & Financial Analytics Community**

</div>
