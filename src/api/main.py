"""
FastAPI Backend for Portfolio Risk Analysis
Provides REST API and WebSocket for real-time VaR calculations
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import json
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.risk_engine.simple_var import calculate_var
import pandas as pd
import numpy as np


# Initialize FastAPI app
app = FastAPI(
    title="Portfolio Risk Analysis API",
    description="Real-time VaR calculations and market data streaming",
    version="1.0.0"
)

# Add CORS middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# MODELS
# ============================================================================

class VaRRequest(BaseModel):
    """Request model for VaR calculation"""
    symbol: str
    prices: List[float]
    confidence_level: Optional[float] = 0.95


class VaRResponse(BaseModel):
    """Response model for VaR calculation"""
    symbol: str
    var_95: float
    var_99: float
    current_price: float
    num_observations: int
    timestamp: str


class SystemStatus(BaseModel):
    """System status model"""
    status: str
    kafka_running: bool
    spark_running: bool
    data_files_count: int
    last_update: str


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_latest_data() -> pd.DataFrame:
    """Load the most recent market data"""
    try:
        # Try to load Kafka/Spark processed data
        data_dir = 'data/processed'
        
        if not os.path.exists(data_dir):
            # Create sample data if no real data exists
            return generate_sample_data()
        
        # Find latest CSV file
        import glob
        files = glob.glob(f'{data_dir}/*.csv')
        
        if not files:
            return generate_sample_data()
        
        latest_file = max(files, key=os.path.getmtime)
        df = pd.read_csv(latest_file)
        
        return df
        
    except Exception as e:
        print(f'Error loading data: {e}')
        return generate_sample_data()


def generate_sample_data() -> pd.DataFrame:
    """Generate sample market data for demo purposes"""
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'JPM']
    data = []
    
    np.random.seed(42)
    
    for symbol in symbols:
        base_price = {'AAPL': 150, 'GOOGL': 140, 'MSFT': 380, 'AMZN': 170, 'JPM': 155}[symbol]
        
        for i in range(100):
            price = base_price + np.random.randn() * 5 + i * 0.1
            data.append({
                'symbol': symbol,
                'price': max(price, 1.0),  # Ensure positive
                'volume': np.random.randint(1000, 10000),
                'timestamp': datetime.now().isoformat()
            })
    
    return pd.DataFrame(data)


def check_kafka_status() -> bool:
    """Check if Kafka is running"""
    try:
        from kafka import KafkaConsumer
        consumer = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            request_timeout_ms=3000
        )
        consumer.close()
        return True
    except:
        return False


def check_spark_status() -> bool:
    """Check if Spark jobs are running"""
    # Simple check - see if checkpoint directory exists and is recent
    checkpoint_dir = 'C:/tmp/checkpoints'
    if os.path.exists(checkpoint_dir):
        # Check if modified in last hour
        import time
        mtime = os.path.getmtime(checkpoint_dir)
        return (time.time() - mtime) < 3600
    return False


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Portfolio Risk Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "var": "/var/{symbol}",
            "calculate_var": "/var/calculate",
            "system_status": "/status",
            "symbols": "/symbols",
            "websocket": "/ws/market-data"
        }
    }


@app.get("/status", response_model=SystemStatus)
async def get_status():
    """Get system status"""
    
    data_dir = 'data/processed'
    file_count = len(os.listdir(data_dir)) if os.path.exists(data_dir) else 0
    
    kafka_running = check_kafka_status()
    spark_running = check_spark_status()
    
    status = "healthy" if (kafka_running or spark_running) else "degraded"
    
    return SystemStatus(
        status=status,
        kafka_running=kafka_running,
        spark_running=spark_running,
        data_files_count=file_count,
        last_update=datetime.now().isoformat()
    )


@app.get("/symbols")
async def get_symbols():
    """Get list of available symbols"""
    df = load_latest_data()
    symbols = df['symbol'].unique().tolist()
    
    return {
        "symbols": symbols,
        "count": len(symbols),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/var/{symbol}", response_model=VaRResponse)
async def get_var(symbol: str):
    """
    Calculate VaR for a specific symbol
    
    Args:
        symbol: Stock symbol (e.g., AAPL, GOOGL)
    
    Returns:
        VaR calculation results
    """
    
    # Load data
    df = load_latest_data()
    
    # Filter for symbol
    symbol_data = df[df['symbol'] == symbol.upper()]
    
    if len(symbol_data) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Symbol '{symbol}' not found"
        )
    
    # Get prices
    prices = symbol_data['price'].values
    
    if len(prices) < 10:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient data for {symbol} (need at least 10 observations)"
        )
    
    # Calculate VaR
    var_95, var_99 = calculate_var(prices, confidence_95=0.95, confidence_99=0.99)
    
    return VaRResponse(
        symbol=symbol.upper(),
        var_95=float(var_95),
        var_99=float(var_99),
        current_price=float(prices[-1]),
        num_observations=len(prices),
        timestamp=datetime.now().isoformat()
    )

@app.post("/var/calculate", response_model=VaRResponse)
async def calculate_var_endpoint(request: VaRRequest):
    """
    Calculate VaR for custom price data
    
    Args:
        request: VaRRequest with symbol and price data
    
    Returns:
        VaR calculation results
    """
    
    if len(request.prices) < 10:
        raise HTTPException(
            status_code=400,
            detail="Need at least 10 price observations"
        )
    
    prices = np.array(request.prices)
    
    # Calculate VaR
    var_95, var_99 = calculate_var(prices)
    
    return VaRResponse(
        symbol=request.symbol,
        var_95=float(var_95),
        var_99=float(var_99),
        current_price=float(prices[-1]),
        num_observations=len(prices),
        timestamp=datetime.now().isoformat()
    )


@app.get("/portfolio/var")
async def get_all_var():
    """Calculate VaR for all symbols"""
    
    df = load_latest_data()
    symbols = df['symbol'].unique()
    
    results = []
    
    for symbol in symbols:
        symbol_data = df[df['symbol'] == symbol]
        prices = symbol_data['price'].values
        
        if len(prices) >= 10:
            var_95, var_99 = calculate_var(prices)
            
            results.append({
                'symbol': symbol,
                'var_95': float(var_95),
                'var_99': float(var_99),
                'current_price': float(prices[-1]),
                'num_observations': len(prices)
            })
    
    return {
        'results': results,
        'count': len(results),
        'timestamp': datetime.now().isoformat()
    }


@app.websocket("/ws/market-data")
async def websocket_market_data(websocket: WebSocket):
    """
    WebSocket endpoint for real-time market data streaming
    
    Sends updated VaR calculations every 5 seconds
    """
    
    await websocket.accept()
    
    try:
        while True:
            # Load latest data
            df = load_latest_data()
            symbols = df['symbol'].unique()
            
            # Calculate VaR for all symbols
            var_data = []
            
            for symbol in symbols:
                symbol_data = df[df['symbol'] == symbol]
                prices = symbol_data['price'].values
                
                if len(prices) >= 10:
                    var_95, var_99 = calculate_var(prices)
                    
                    var_data.append({
                        'symbol': symbol,
                        'var_95': float(var_95),
                        'var_99': float(var_99),
                        'current_price': float(prices[-1]),
                        'timestamp': datetime.now().isoformat()
                    })
            
            # Send data
            await websocket.send_json({
                'type': 'var_update',
                'data': var_data,
                'timestamp': datetime.now().isoformat()
            })
            
            # Wait 5 seconds
            await asyncio.sleep(5)
            
    except Exception as e:
        print(f'WebSocket error: {e}')
    finally:
        await websocket.close()


# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("=" * 80)
    print("PORTFOLIO RISK ANALYSIS API")
    print("=" * 80)
    print()
    print("API running at: http://localhost:8000")
    print("Docs available at: http://localhost:8000/docs")
    print()
    print("Endpoints:")
    print("  GET  /status              - System status")
    print("  GET  /symbols             - List available symbols")
    print("  GET  /var/{symbol}        - Get VaR for symbol")
    print("  POST /var/calculate       - Calculate custom VaR")
    print("  GET  /var/all             - Get VaR for all symbols")
    print("  WS   /ws/market-data      - Real-time WebSocket")
    print()
    print("=" * 80)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)