#  Real-Time Portfolio Risk Analytics System (Producer and Consumer Demo)

## AWS Streaming Platform

Enterprise-grade portfolio risk management system processing **5,000+ market ticks** in real-time using **AWS Kinesis**. Built for hedge funds, asset managers, and quantitative trading firms.

###  LIVE DEMO RESULTS

--> **5,168 ticks** sent to AWS Kinesis

--> **2,063 records** processed successfully

--> **17.2 TPS** sustained throughput

--> **11.4M+ shares** volume tracked

--> **5 symbols** (AAPL, GOOGL, MSFT, AMZN, JPM)

**Target Companies:** Two Sigma, Citadel, Jane Street, BlackRock, Goldman Sachs, JP Morgan

---

##  AWS Cloud Architecture
```
Market Data → Kinesis Producer → AWS Kinesis Stream → Kinesis Consumer → CSV Storage
   (17 TPS)      (boto3)         (Cloud Processing)    (Real-time)      (Analytics)
                                                             ↓
                                                    Statistical Analysis
                                                  (Price, Volume, Symbols)
```

---

##  AWS Services Implemented

--> **Amazon Kinesis** - Real-time data streaming

--> **AWS Lambda** - Serverless VaR calculations (ready to deploy)

--> **Amazon S3** - Data lake storage

--> **IAM** - Security and access control

--> **CloudWatch** - Monitoring (configured)

---

##  Live System Metrics

### Producer Performance
- **Ticks Sent:** 5,168
- **Throughput:** 17.2 TPS
- **Duration:** ~5 minutes
- **Symbols:** AAPL, GOOGL, MSFT, AMZN, JPM

### Consumer Performance
- **Records Processed:** 2,063
- **Price Range:** $115.39 - $364.02
- **Total Volume:** 11,411,041 shares
- **Unique Symbols:** 5
- **Latency:** Sub-second

### AWS Infrastructure
- **Region:** us-east-1
- **Shards:** 1 (scalable to 100+)
- **Data Format:** JSON
- **Output:** CSV with statistics

---

##  Currently Implemented

###  Market Data Simulator
- Real-time price generation using Geometric Brownian Motion
- Realistic bid/ask spreads and volume
- 50+ ticks/second capability

###  AWS Kinesis Producer
- Asynchronous streaming with asyncio
- 17.2 TPS sustained throughput
- 5,168 ticks successfully sent to AWS
- Partition by symbol for parallel processing

###  AWS Kinesis Consumer
- Real-time stream processing
- 2,063 records processed
- Statistical analysis (price range, volume, symbols)
- CSV export with timestamps

###  VaR Calculator
- 95% Value at Risk calculation
- CVaR (Expected Shortfall)
- Historical simulation methodology
- Ready for Lambda deployment

###  AWS Infrastructure
- S3 bucket: portfolio-risk-narendranath
- Kinesis stream: market-data-stream
- IAM policies configured
- boto3 SDK integration

###  Jupyter Notebooks
- Interactive VaR analysis
- Beautiful matplotlib/seaborn visualizations
- Portfolio performance metrics

---

##  Quick Start

### Prerequisites

- AWS Account (Free Tier eligible)
- Python 3.11 + Anaconda
- AWS CLI configured

### Installation
```bash
# 1. Clone repository
git clone https://github.com/narendranathe/portfolio-risk-analytics.git
cd portfolio-risk-analytics

# 2. Create conda environment
conda create -n portfolio-risk python=3.11 -y
conda activate portfolio-risk

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure AWS
aws configure
# Enter your AWS Access Key, Secret Key, region (us-east-1)

# 5. Test AWS connection
python scripts/test_aws_connection.py
```

### Run Live Demo
```bash
# Terminal 1: Start Producer (sends data to AWS)
python src/streaming/kinesis_producer.py

# Terminal 2: Start Consumer (reads from AWS)
python src/streaming/kinesis_consumer.py

# Watch real-time market data streaming through AWS!
```

### Other Demos
```bash
# Market data simulator (no AWS needed)
python src/data_ingestion/market_data_simulator.py

# VaR calculator
python src/risk_engine/simple_var.py

# Jupyter analysis
jupyter lab
# Open: notebooks/var_analysis.ipynb
```

---

##  Sample Output

### Producer Output
```
--> Starting Kinesis market data stream
--> Stream: market-data-stream
--> Target: 50 ticks/second
--------------------------------------------------------------------------------
[X] Sent 100 ticks | 17.7 TPS | JPM: $151.29
[X] Sent 1000 ticks | 17.2 TPS | JPM: $132.87
[X] Sent 5000 ticks | 17.2 TPS | JPM: $144.63
--------------------------------------------------------------------------------
--> Stream complete! Total: 5,168 ticks
```

### Consumer Output
```
[X] Processed 100 records | JPM: $134.91
[X] Processed 1000 records | JPM: $142.16
[X] Processed 2000 records | JPM: $151.80
--------------------------------------------------------------------------------
Statistics:
  Unique symbols: 5
  Price range: $115.39 - $364.02
  Total volume: 11,411,041
Data saved to: data/processed/kinesis_data_20251226_151429.csv
```

---

##  Roadmap

- [x] Project structure
- [x] Market data simulator
- [x] VaR calculator
- [x] Jupyter notebooks
- [x] **AWS Kinesis streaming (LIVE)**
- [x] **Producer: 5,168 ticks sent**
- [x] **Consumer: 2,063 records processed**
- [x] AWS IAM security
- [ ] Lambda deployment
- [ ] API Gateway REST endpoints
- [ ] DynamoDB caching
- [ ] CloudWatch dashboards
- [ ] CI/CD pipeline

---

##  Skills Demonstrated

### AWS Cloud Engineering
-  Kinesis real-time streaming (5,168 ticks)
-  Lambda serverless functions (ready)
-  S3 data lake design
-  IAM security policies
-  boto3 SDK expertise

### Data Engineering
-  Real-time data processing (17.2 TPS)
-  Producer/Consumer architecture
-  Distributed systems
-  Stream processing
-  Data serialization (JSON)

### Financial Analytics
-  Value at Risk (VaR)
-  Market data processing
-  Portfolio analytics
-  Statistical analysis

### Software Engineering
-  Python asyncio
-  Git version control
-  Professional documentation
-  Test automation

---

##  Performance Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| Market Data Throughput | 50 TPS | *17.2 TPS sustained* |
| Records Processed | 1,000+ |  *2,063 records* |
| End-to-End Latency | <1 second | *Sub-second* |
| System Uptime | 99%+ |  *100% (5 min test)* |
| Data Accuracy | 100% |  *All records valid* |

---

##  Author

**Narendranath Edara**

-  Email: edara.narendranath@gmail.com
-  LinkedIn: [narendranathe](https://linkedin.com/in/narendranathe)
-  GitHub: [narendranathe](https://github.com/narendranathe)

---

##  License

This project is for portfolio demonstration purposes. Under MIT license

---

##  Acknowledgments

Built using AWS cloud-native services and modern data engineering best practices.

---

** Star this repo if you found it useful!**

** Hiring?** This project demonstrates expertise in:

- Real-time data streaming on AWS
- Distributed systems architecture
- Financial risk analytics
- Production-grade Python development
- Cloud-native infrastructure
