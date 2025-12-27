"""
Simple Kafka Consumer for Testing
"""

from kafka import KafkaConsumer
import json


def consume_market_data():
    print('=' * 80)
    print('KAFKA CONSUMER (Simple Test)')
    print('=' * 80)
    print()
    
    consumer = KafkaConsumer(
        'market-data',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        group_id='test-consumer'
    )
    
    print('Consuming messages from topic: market-data')
    print('Press Ctrl+C to stop')
    print('-' * 80)
    
    count = 0
    try:
        for message in consumer:
            data = message.value
            count += 1
            
            if count % 10 == 0:
                symbol = data['symbol']
                price = data['price']
                volume = data['volume']
                msg = 'Received {} messages | {}: ${:.2f} | Vol: {:,}'
                print(msg.format(count, symbol, price, volume))
    
    except KeyboardInterrupt:
        print()
        print('-' * 80)
        print('Consumed {} total messages'.format(count))
        consumer.close()


if __name__ == '__main__':
    consume_market_data()
