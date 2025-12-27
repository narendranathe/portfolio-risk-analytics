"""
Kafka Producer for Market Data Streaming
Production-ready implementation with error handling
"""

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import json
import time
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data_ingestion.market_data_simulator import MarketDataSimulator


class KafkaMarketDataProducer:
    def __init__(self, bootstrap_servers='localhost:9092', topic='market-data'):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.records_sent = 0
        
        # Create topic if not exists
        self.create_topic()
        
        # Initialize producer
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',
            retries=3,
            max_in_flight_requests_per_connection=5,
            compression_type='gzip'
        )
        
        self.simulator = MarketDataSimulator()
        print('Kafka producer connected to', bootstrap_servers)
    
    def create_topic(self):
        try:
            admin = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
            topic = NewTopic(
                name=self.topic,
                num_partitions=5,
                replication_factor=1
            )
            admin.create_topics([topic])
            print('Created topic:', self.topic)
        except TopicAlreadyExistsError:
            print('Topic already exists:', self.topic)
        except Exception as e:
            print('Topic creation:', str(e))
    
    def send_tick(self, tick):
        data = {
            'symbol': tick.symbol,
            'timestamp': tick.timestamp,
            'price': tick.price,
            'volume': tick.volume,
            'bid': tick.bid,
            'ask': tick.ask
        }
        
        future = self.producer.send(
            self.topic,
            key=tick.symbol,
            value=data
        )
        
        self.records_sent += 1
        return future
    
    def stream_market_data(self, duration_seconds=300, ticks_per_second=50):
        print('=' * 80)
        print('KAFKA MARKET DATA PRODUCER')
        print('=' * 80)
        print('Topic:', self.topic)
        print('Target:', ticks_per_second, 'TPS for', duration_seconds, 'seconds')
        print('Bootstrap:', self.bootstrap_servers)
        print('-' * 80)
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        tick_interval = 1.0 / ticks_per_second
        
        try:
            while time.time() < end_time:
                iteration_start = time.time()
                
                symbol = self.simulator.symbols[self.records_sent % len(self.simulator.symbols)]
                tick = self.simulator.generate_tick(symbol)
                self.send_tick(tick)
                
                if self.records_sent % 100 == 0:
                    elapsed = time.time() - start_time
                    actual_tps = self.records_sent / elapsed
                    msg = 'Sent {} ticks | {:.1f} TPS | {}: ${:.2f}'
                    print(msg.format(self.records_sent, actual_tps, tick.symbol, tick.price))
                
                elapsed = time.time() - iteration_start
                sleep_time = max(0, tick_interval - elapsed)
                time.sleep(sleep_time)
        
        except KeyboardInterrupt:
            print('Stopped by user')
        
        finally:
            self.producer.flush()
            
            print('-' * 80)
            print('Stream complete!')
            print('Total ticks sent:', self.records_sent)
            total_time = time.time() - start_time
            print('Average TPS: {:.1f}'.format(self.records_sent / total_time))
            
            self.producer.close()


if __name__ == '__main__':
    producer = KafkaMarketDataProducer()
    producer.stream_market_data(duration_seconds=300, ticks_per_second=50)