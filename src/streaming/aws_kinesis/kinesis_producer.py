"""
AWS Kinesis Producer for Real-time Market Data Streaming
Replaces Kafka with AWS-native streaming
"""

import boto3
import json
import asyncio
import time
from datetime import datetime
from typing import List
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data_ingestion.market_data_simulator import MarketDataSimulator, MarketTick


class KinesisMarketDataProducer:
    """Stream market data to AWS Kinesis"""
    
    def __init__(self, stream_name: str = 'market-data-stream', region: str = 'us-east-1'):
        self.stream_name = stream_name
        self.kinesis_client = boto3.client('kinesis', region_name=region)
        self.simulator = MarketDataSimulator()
        self.records_sent = 0
        
    def create_stream_if_not_exists(self, shard_count: int = 1):
        """Create Kinesis stream if it doesn't exist"""
        try:
            # Check if stream exists
            self.kinesis_client.describe_stream(StreamName=self.stream_name)
            print(f'✅ Stream {self.stream_name} already exists')
            
        except self.kinesis_client.exceptions.ResourceNotFoundException:
            # Create stream
            print(f'Creating Kinesis stream: {self.stream_name}')
            self.kinesis_client.create_stream(
                StreamName=self.stream_name,
                ShardCount=shard_count
            )
            
            # Wait for stream to become active
            print('Waiting for stream to become active...')
            waiter = self.kinesis_client.get_waiter('stream_exists')
            waiter.wait(StreamName=self.stream_name)
            print(f'✅ Stream {self.stream_name} created successfully')
    
    def send_tick(self, tick: MarketTick) -> bool:
        """Send single market tick to Kinesis"""
        try:
            # Convert tick to JSON
            data = json.dumps({
                'symbol': tick.symbol,
                'timestamp': tick.timestamp,
                'price': tick.price,
                'volume': tick.volume,
                'bid': tick.bid,
                'ask': tick.ask
            })
            
            # Send to Kinesis
            response = self.kinesis_client.put_record(
                StreamName=self.stream_name,
                Data=data,
                PartitionKey=tick.symbol
            )
            
            self.records_sent += 1
            return True
            
        except Exception as e:
            print(f'❌ Error sending tick: {e}')
            return False
    
    async def stream_market_data(self, duration_seconds: int = 300, 
                                 ticks_per_second: int = 50):
        """Stream market data to Kinesis"""
        print(f'🚀 Starting Kinesis market data stream')
        print(f'📊 Stream: {self.stream_name}')
        print(f'⚡ Target: {ticks_per_second} ticks/second for {duration_seconds}s')
        print('-' * 80)
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        tick_interval = 1.0 / ticks_per_second
        
        while time.time() < end_time:
            iteration_start = time.time()
            
            # Generate tick
            symbol = self.simulator.symbols[self.records_sent % len(self.simulator.symbols)]
            tick = self.simulator.generate_tick(symbol)
            
            # Send to Kinesis
            self.send_tick(tick)
            
            # Progress logging
            if self.records_sent % 100 == 0:
                elapsed = time.time() - start_time
                actual_tps = self.records_sent / elapsed
                print(f'📤 Sent {self.records_sent} ticks | {actual_tps:.1f} TPS | '
                      f'{tick.symbol}: ${tick.price:.2f}')
            
            # Sleep to maintain target TPS
            elapsed = time.time() - iteration_start
            sleep_time = max(0, tick_interval - elapsed)
            await asyncio.sleep(sleep_time)
        
        print('-' * 80)
        print(f'✅ Stream complete!')
        print(f'📈 Total ticks sent: {self.records_sent}')
        print(f'⚡ Average TPS: {self.records_sent / duration_seconds:.1f}')


async def main():
    """Run Kinesis producer"""
    print('=' * 80)
    print('AWS KINESIS MARKET DATA PRODUCER')
    print('=' * 80)
    print()
    
    producer = KinesisMarketDataProducer()
    
    # Create stream if needed
    producer.create_stream_if_not_exists(shard_count=1)
    
    print()
    print('Starting data stream...')
    print('Press Ctrl+C to stop early')
    print()
    
    try:
        # Stream for 5 minutes at 50 ticks/second
        await producer.stream_market_data(
            duration_seconds=300,
            ticks_per_second=50
        )
    except KeyboardInterrupt:
        print('\n⏹️  Stopped by user')
        print(f'📊 Total records sent: {producer.records_sent}')


if __name__ == '__main__':
    asyncio.run(main())
