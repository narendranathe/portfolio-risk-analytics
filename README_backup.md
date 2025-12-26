# 🎯 Real-Time Portfolio Risk Analytics System

## Overview

Production-ready portfolio risk management system . Processes real-time market data, calculates Value at Risk (VaR), and provides ML-based portfolio optimization.

## 🚀 Tech Stack

- **Data Processing**: Python, NumPy, Pandas
- **Financial Analytics**: Custom VaR models, risk metrics
- **Streaming** (Coming): Apache Kafka, Spark Streaming
- **ML** (Coming): Scikit-learn, XGBoost, MLflow
- **Orchestration** (Coming): Apache Airflow
- **Cloud** (Coming): Databricks, Azure
- **Infrastructure**: Docker, Anaconda

## 📊 Currently Implemented

✅ **Market Data Simulator**
- Generates realistic stock price movements
- Simulates bid/ask spreads
- Processes 10+ ticks per second
- Supports AAPL, GOOGL, MSFT, AMZN, JPM

✅ **VaR Calculator**
- 95% Value at Risk calculation
- Conditional VaR (Expected Shortfall)
- Historical simulation method
- Portfolio risk metrics

## 🛠️ Quick Start

### Prerequisites
- Anaconda Python 3.x
- Windows 10/11

### Installation
```bash
# 1. Clone repository
git clone https://github.com/narendranathe/portfolio-risk-analytics.git
cd portfolio-risk-analytics

# 2. Create conda environment
conda create -n portfolio-risk python=3.11 -y
conda activate portfolio-risk

# 3. Install dependencies
conda install numpy pandas scipy -y

# 4. Run tests
python scripts\test_basic.py
```

### Run Demos
```bash
# Market data stream (30 seconds)
python src\data_ingestion\market_data_simulator.py

# VaR calculation demo
python src\risk_engine\simple_var.py
```

## 📈 Demo Output

### Market Data Stream
```
Starting market data stream for 30 seconds
Symbols: AAPL, GOOGL, MSFT, AMZN, JPM
--------------------------------------------------------------------------------
AAPL   | $180.45 | Bid: $180.43 | Ask: $180.47 | Vol:  5432
GOOGL  | $140.23 | Bid: $140.21 | Ask: $140.25 | Vol:  7891
...
```

### VaR Calculation
```
Portfolio Value: $10,000,000
95% VaR: $256,834.21
CVaR (Expected Shortfall): $312,445.67
```

## 📚 Project Structure
```
portfolio-risk-analytics/
├── src/
│   ├── data_ingestion/
│   │   └── market_data_simulator.py    ✅ Working
│   └── risk_engine/
│       └── simple_var.py                ✅ Working
├── scripts/
│   └── test_basic.py                    ✅ Working
├── tests/
├── docs/
└── README.md
```

## 🎯 Roadmap

- [x] Project structure setup
- [x] Market data simulator
- [x] Basic VaR calculator
- [ ] Kafka streaming integration
- [ ] Spark processing pipeline
- [ ] ML models (XGBoost, LSTM)
- [ ] Databricks notebooks
- [ ] Airflow orchestration
- [ ] FastAPI REST API
- [ ] Grafana monitoring

## 🏆 Skills Demonstrated

**Financial Analytics:**
- Value at Risk (VaR) calculation
- Risk metrics and portfolio analytics
- Market data processing

**Data Engineering:**
- Real-time data simulation
- Python OOP design patterns
- Test-driven development

**Coming Soon:**
- Distributed processing (Spark)
- Stream processing (Kafka)
- ML deployment (MLflow)
- Cloud architecture (Databricks)

## 👤 Author

**Narendranath Edara**
- 📧 Email: edara.narendranath@gmail.com
- 💼 LinkedIn: [narendranathe](https://linkedin.com/in/narendranathe)
- 🐙 GitHub: [narendranathe](https://github.com/narendranathe)

## 📝 License

This project is for portfolio demonstration purposes.

---

**⭐ Star this repo if you found it useful!**
