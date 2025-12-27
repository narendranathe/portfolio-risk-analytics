"""
Spark Kafka Streaming - WORKING VERSION
"""

import os
import sys

# Set Python for Spark workers
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-11'
os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['SPARK_LOCAL_DIRS'] = r'C:\tmp'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def main():
    print('=' * 80)
    print('SPARK KAFKA STREAMING - PRODUCTION VERSION')
    print('=' * 80)
    print()
    
    # Create Spark with Kafka package
    print('Initializing Spark with Kafka support...')
    
    spark = SparkSession.builder \
        .appName('PortfolioRiskKafka') \
        .master('local[2]') \
        .config('spark.driver.host', '127.0.0.1') \
        .config('spark.driver.bindAddress', '127.0.0.1') \
        .config('spark.sql.warehouse.dir', 'file:///C:/tmp/spark-warehouse') \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
        .config('spark.ui.enabled', 'false') \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel('WARN')
    
    print('✅ Spark session ready')
    print('   Version:', spark.version)
    print()
    
    # Define schema
    schema = StructType([
        StructField('symbol', StringType()),
        StructField('timestamp', StringType()),
        StructField('price', DoubleType()),
        StructField('volume', IntegerType()),
        StructField('bid', DoubleType()),
        StructField('ask', DoubleType())
    ])
    
    # Read from Kafka
    print('Connecting to Kafka at localhost:9092...')
    print('Topic: market-data')
    print()
    
    try:
        df = spark.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'localhost:9092') \
            .option('subscribe', 'market-data') \
            .option('startingOffsets', 'latest') \
            .load()
        
        print('✅ Connected to Kafka!')
        print()
        
        # Parse JSON
        parsed_df = df.select(
            from_json(col('value').cast('string'), schema).alias('data')
        ).select('data.*')
        
        # Add processing time
        enriched_df = parsed_df.withColumn('processing_time', current_timestamp())
        
        # 5-second windowed aggregations
        stats_df = enriched_df \
            .withWatermark('processing_time', '10 seconds') \
            .groupBy(
                window('processing_time', '5 seconds'),
                'symbol'
            ) \
            .agg(
                count('*').alias('ticks'),
                round(avg('price'), 2).alias('avg_price'),
                round(min('price'), 2).alias('min_price'),
                round(max('price'), 2).alias('max_price'),
                sum('volume').alias('volume')
            )
        
        print('Starting 5-second windowed aggregations...')
        print('Press Ctrl+C to stop')
        print('-' * 80)
        print()
        
        # Output to console
        query = stats_df.writeStream \
            .outputMode('update') \
            .format('console') \
            .option('truncate', False) \
            .trigger(processingTime='5 seconds') \
            .start()
        
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
    main()