"""
Delta Lake Writer - WORKING VERSION
"""

import os
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['HADOOP_HOME'] = r'C:\\hadoop'
os.environ['JAVA_HOME'] = r'C:\\Program Files\\Java\\jdk-11'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from delta import *


def create_spark_with_delta():
    print('Initializing Spark with Kafka + Delta Lake...')
    
    builder = SparkSession.builder \
        .appName('DeltaLakeKafka') \
        .master('local[2]') \
        .config('spark.driver.host', '127.0.0.1') \
        .config('spark.driver.bindAddress', '127.0.0.1') \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,io.delta:delta-spark_2.12:3.1.0') \
        .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
        .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
        .config('spark.ui.enabled', 'false')
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    return spark


def main():
    print('=' * 80)
    print('DELTA LAKE STREAMING')
    print('=' * 80)
    print()
    
    BRONZE_PATH = 'C:/tmp/delta/bronze/market-data'
    
    print('Bronze Path:', BRONZE_PATH)
    print()
    
    spark = create_spark_with_delta()
    print('Spark initialized')
    print()
    
    schema = StructType([
        StructField('symbol', StringType()),
        StructField('timestamp', StringType()),
        StructField('price', DoubleType()),
        StructField('volume', IntegerType()),
        StructField('bid', DoubleType()),
        StructField('ask', DoubleType())
    ])
    
    print('Connecting to Kafka...')
    kafka_df = spark.readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', 'localhost:9092') \
        .option('subscribe', 'market-data') \
        .option('startingOffsets', 'latest') \
        .load()
    
    print('Connected to Kafka')
    print()
    
    parsed_df = kafka_df.select(
        from_json(col('value').cast('string'), schema).alias('data'),
        col('timestamp').alias('kafka_timestamp')
    ).select('data.*', 'kafka_timestamp')
    
    bronze_df = parsed_df.withColumn('ingestion_time', current_timestamp())
    
    print('Starting Bronze layer...')
    
    bronze_query = bronze_df.writeStream \
        .format('delta') \
        .outputMode('append') \
        .option('checkpointLocation', 'C:/tmp/checkpoints/bronze') \
        .option('path', BRONZE_PATH) \
        .trigger(processingTime='10 seconds') \
        .start()
    
    print('Bronze layer running!')
    print('Press Ctrl+C to stop')
    print()
    
    try:
        bronze_query.awaitTermination()
    except KeyboardInterrupt:
        print('\\nStopping...')
        bronze_query.stop()
        spark.stop()
        print('Stopped')


if __name__ == '__main__':
    main()
