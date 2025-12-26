"""
AWS Kinesis Consumer for Market Data Processing
"""

import boto3
import json
import time
from typing import Dict, List
import pandas as pd
from datetime import datetime


class KinesisMarketDataConsumer:
    def __init__(self, stream_name='market-data-stream', region='us-east-1'):
        self.stream_name = stream_name
        self.kinesis_client = boto3.client('kinesis', region_name=region)
        self.records_processed = 0
        
    def get_shard_iterator(self, shard_id):
        response = self.kinesis_client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=shard_id,
            ShardIteratorType='LATEST'
        )
        return response['ShardIterator']
    
    def process_record(self, record):
        data = json.loads(record['Data'])
        data['kinesis_timestamp'] = str(record['ApproximateArrivalTimestamp'])
        data['sequence_number'] = record['SequenceNumber']
        return data
    
    def consume_stream(self, duration_seconds=120):
        print('=' * 80)
        print('AWS KINESIS MARKET DATA CONSUMER')
        print('=' * 80)
        print()
        print('Starting Kinesis consumer')
        print('Stream:', self.stream_name)
        print('Duration:', duration_seconds, 'seconds')
        print('-' * 80)
        
        response = self.kinesis_client.describe_stream(StreamName=self.stream_name)
        shards = response['StreamDescription']['Shards']
        
        print('Found', len(shards), 'shard(s)')
        print()
        
        shard_id = shards[0]['ShardId']
        shard_iterator = self.get_shard_iterator(shard_id)
        
        start_time = time.time()
        all_records = []
        
        print('Consuming records...')
        print()
        
        while time.time() - start_time < duration_seconds:
            try:
                response = self.kinesis_client.get_records(
                    ShardIterator=shard_iterator,
                    Limit=100
                )
                
                records = response['Records']
                
                if records:
                    for record in records:
                        processed = self.process_record(record)
                        all_records.append(processed)
                        self.records_processed += 1
                        
                        if self.records_processed % 10 == 0:
                            symbol = processed['symbol']
                            price = processed['price']
                            msg = 'Processed {} records | {}: ${:.2f}'
                            print(msg.format(self.records_processed, symbol, price))
                
                shard_iterator = response['NextShardIterator']
                
                if not shard_iterator:
                    print('No more data available')
                    break
                
                time.sleep(1)
                
            except Exception as e:
                print('Error:', str(e))
                break
        
        print()
        print('-' * 80)
        print('Consumer complete!')
        print('Total records processed:', self.records_processed)
        
        if all_records:
            df = pd.DataFrame(all_records)
            print()
            print('Sample data:')
            print(df.head(10))
            
            print()
            print('Statistics:')
            print('  Unique symbols:', df['symbol'].nunique())
            print('  Price range: ${:.2f} - ${:.2f}'.format(df['price'].min(), df['price'].max()))
            print('  Total volume: {:,}'.format(df['volume'].sum()))
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = 'data/processed/kinesis_data_{}.csv'.format(timestamp)
            df.to_csv(output_file, index=False)
            print()
            print('Data saved to:', output_file)
        else:
            print()
            print('No records received. Make sure producer is running!')
        
        return all_records


if __name__ == '__main__':
    consumer = KinesisMarketDataConsumer()
    consumer.consume_stream(duration_seconds=120)