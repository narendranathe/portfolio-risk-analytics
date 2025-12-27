"""
Spark Streaming - Self-Configuring for Windows
"""

import os
import sys

# Force set environment variables BEFORE importing Spark
os.environ['HADOOP_HOME'] = 'C:\\hadoop'
os.environ['SPARK_LOCAL_DIRS'] = 'C:\\tmp'
os.environ['SPARK_TMP_DIR'] = 'C:\\tmp'

# Verify settings
print('=' * 80)
print('SPARK CONFIGURATION CHECK')
print('=' * 80)
print('HADOOP_HOME:', os.environ.get('HADOOP_HOME'))
print('SPARK_LOCAL_DIRS:', os.environ.get('SPARK_LOCAL_DIRS'))
print()

# Check files exist
import os.path
winutils_path = 'C:\\hadoop\\bin\\winutils.exe'
hadoop_dll_path = 'C:\\hadoop\\bin\\hadoop.dll'

print('Checking required files:')
print('  winutils.exe:', '✅ Found' if os.path.exists(winutils_path) else '❌ Missing')
print('  hadoop.dll:', '✅ Found' if os.path.exists(hadoop_dll_path) else '❌ Missing')
print()

# Now import Spark
print('Importing PySpark...')
try:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    print('✅ PySpark imported')
    print()
except Exception as e:
    print('❌ Failed to import PySpark:', e)
    sys.exit(1)

# Create Spark session
print('Creating Spark session...')
try:
    spark = SparkSession.builder \
        .appName('PortfolioRisk') \
        .master('local[2]') \
        .config('spark.driver.host', 'localhost') \
        .config('spark.driver.bindAddress', '127.0.0.1') \
        .config('spark.sql.warehouse.dir', 'file:///C:/tmp/spark-warehouse') \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
        .config('spark.ui.enabled', 'false') \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel('ERROR')
    print('✅ Spark session created!')
    print('   Version:', spark.version)
    print()
    
except Exception as e:
    print('❌ Failed to create Spark session')
    print('Error:', e)
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test basic operation
print('Testing basic operation...')
try:
    data = [('Alice', 25), ('Bob', 30)]
    df = spark.createDataFrame(data, ['name', 'age'])
    print('✅ Basic DataFrame test passed')
    df.show()
    print()
except Exception as e:
    print('❌ Basic test failed:', e)
    spark.stop()
    sys.exit(1)

# Now try Kafka streaming
print('=' * 80)
print('STARTING KAFKA STREAM PROCESSING')
print('=' * 80)
print()

schema = StructType([
    StructField('symbol', StringType()),
    StructField('timestamp', StringType()),
    StructField('price', DoubleType()),
    StructField('volume', IntegerType()),
    StructField('bid', DoubleType()),
    StructField('ask', DoubleType())
])

try:
    print('Connecting to Kafka at localhost:9092...')
    df = spark.readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', 'localhost:9092') \
        .option('subscribe', 'market-data') \
        .option('startingOffsets', 'latest') \
        .load()
    
    print('✅ Connected to Kafka')
    print()
    
    # Parse JSON
    parsed = df.select(
        from_json(col('value').cast('string'), schema).alias('data')
    ).select('data.*')
    
    # Count by symbol
    stats = parsed.groupBy('symbol').count()
    
    print('Starting stream output...')
    print('Press Ctrl+C to stop')
    print('-' * 80)
    
    query = stats.writeStream \
        .outputMode('complete') \
        .format('console') \
        .option('truncate', False) \
        .start()
    
    query.awaitTermination()
    
except KeyboardInterrupt:
    print('\n⏹️  Stopping...')
    query.stop()
    spark.stop()
    print('✅ Stopped')
    
except Exception as e:
    print('❌ Streaming error:', e)
    import traceback
    traceback.print_exc()
    spark.stop()