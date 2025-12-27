"""
Simplified Spark Streaming Consumer (No Checkpoints)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def process_streaming_data():
    print('=' * 80)
    print('SPARK STRUCTURED STREAMING CONSUMER')
    print('=' * 80)
    print()
    
    # Create Spark session
    spark = SparkSession.builder \
        .appName('PortfolioRiskAnalytics') \
        .master('local[*]') \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel('WARN')
    
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
    print('Reading from Kafka...')
    df = spark.readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', 'localhost:9092') \
        .option('subscribe', 'market-data') \
        .option('startingOffsets', 'latest') \
        .load()
    
    # Parse JSON
    parsed = df.select(
        from_json(col('value').cast('string'), schema).alias('data')
    ).select('data.*')
    
    # Simple aggregation
    stats = parsed.groupBy('symbol').count()
    
    # Output to console
    print('Starting stream...')
    query = stats.writeStream \
        .outputMode('complete') \
        .format('console') \
        .start()
    
    print('Press Ctrl+C to stop')
    
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print('\nStopping...')
        query.stop()
        spark.stop()


if __name__ == '__main__':
    process_streaming_data()

