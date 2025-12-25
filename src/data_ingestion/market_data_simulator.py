"""
Simple market data simulator for testing
Generates realistic stock price movements
"""

import random
import time
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MarketTick:
    """Single market data tick"""
    symbol: str
    timestamp: str
    price: float
    volume: int
    bid: float
    ask: float


class MarketDataSimulator:
    """Simulates real-time market data"""
    
    def __init__(self):
        self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'JPM']
        self.prices = {
            'AAPL': 180.0,
            'GOOGL': 140.0,
            'MSFT': 380.0,
            'AMZN': 170.0,
            'JPM': 150.0
        }
    
    def generate_tick(self, symbol):
        current_price = self.prices[symbol]
        price_change = current_price * random.uniform(-0.01, 0.01)
        new_price = current_price + price_change
        self.prices[symbol] = new_price
        
        spread = new_price * 0.0001
        bid = new_price - spread
        ask = new_price + spread
        volume = random.randint(1000, 10000)
        
        return MarketTick(
            symbol=symbol,
            timestamp=datetime.now().isoformat(),
            price=round(new_price, 2),
            volume=volume,
            bid=round(bid, 2),
            ask=round(ask, 2)
        )
    
    def stream_data(self, duration_seconds=60):
        print(f"Starting market data stream for {duration_seconds} seconds")
        print(f"Symbols: {', '.join(self.symbols)}")
        print("-" * 80)
        
        start_time = time.time()
        tick_count = 0
        
        while time.time() - start_time < duration_seconds:
            symbol = random.choice(self.symbols)
            tick = self.generate_tick(symbol)
            
            print(f"{tick.symbol:6} | ${tick.price:7.2f} | Bid: ${tick.bid:7.2f} | Ask: ${tick.ask:7.2f} | Vol: {tick.volume:5}")
            
            tick_count += 1
            time.sleep(0.1)
        
        elapsed = time.time() - start_time
        tps = tick_count / elapsed
        
        print("-" * 80)
        print(f"Stream complete! Total ticks: {tick_count}, TPS: {tps:.1f}")


if __name__ == "__main__":
    simulator = MarketDataSimulator()
    simulator.stream_data(duration_seconds=30)
