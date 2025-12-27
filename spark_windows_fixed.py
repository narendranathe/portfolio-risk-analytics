"""
Spark Streaming - Windows Fixed Version
"""

import os
import sys

# Set up environment for Windows
os.environ['HADOOP_HOME'] = 'C:\\hadoop'
os.environ['SPARK_LOCAL_DIRS'] = 'C:\\tmp'

# Add to path
if 'C:\\hadoop\\bin' not in os.environ['PATH']:
    os.environ['PATH'] = 'C:\\hadoop\\bin;' + os.environ['PATH']

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def create_spark():
    print('Creating Spark session for Windows...')
    
    spark = SparkSession.builder \
        .appName('PortfolioRisk') \
        .master('local[2]') \
        .config('spark.driver.host', 'localhost') \
        .config('spark.driver.bindAddress', '127.0.0.1') \
        .config('spark.sql.warehouse.dir', 'file:///C:/tmp/spark-warehouse') \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
        .config('spark.driver.extraJavaOptions', '-Djava.io.tmpdir=C:/tmp') \
        .config('spark.executor.extraJavaOptions', '-Djava.io.tmpdir=C:/tmp') \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel('ERROR')
    return spark


def process_stream():
    print('=' * 80)
    print('SPARK STRUCTURED STREAMING - WINDOWS VERSION')
    print('=' * 80)
    print()
    
    spark = create_spark()
    print('✅ Spark session created!')
    print()
    
    schema = StructType([
        StructField('symbol', StringType()),
        StructField('timestamp', StringType()),
        StructField('price', DoubleType()),
        StructField('volume', IntegerType()),
        StructField('bid', DoubleType()),
        StructField('ask', DoubleType())
    ])
    
    print('Reading from Kafka topic: market-data')
    
    try:
        df = spark.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'localhost:9092') \
            .option('subscribe', 'market-data') \
            .option('startingOffsets', 'latest') \
            .load()
        
        parsed = df.select(
            from_json(col('value').cast('string'), schema).alias('data')
        ).select('data.*')
        
        stats = parsed.groupBy('symbol').count()
        
        print('Starting stream output...')
        print('-' * 80)
        
        query = stats.writeStream \
            .outputMode('complete') \
            .format('console') \
            .option('truncate', False) \
            .start()
        
        print('✅ Streaming started! Press Ctrl+C to stop')
        print()
        
        query.awaitTermination()
        
    except KeyboardInterrupt:
        print('\n⏹️  Stopping...')
        query.stop()
        spark.stop()
        print('✅ Stopped')
    except Exception as e:
        print('❌ Error:', e)
        import traceback
        traceback.print_exc()
        spark.stop()


if __name__ == '__main__':
    process_stream()