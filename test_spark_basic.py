"""
Step-by-step Spark test
"""

import os
import sys

print('=' * 80)
print('SPARK STEP-BY-STEP TEST')
print('=' * 80)
print()

# Step 1: Set environment
print('Step 1: Setting environment variables...')
os.environ['HADOOP_HOME'] = 'C:\\hadoop'
os.environ['SPARK_LOCAL_DIRS'] = 'C:\\tmp'
print('  ✅ HADOOP_HOME:', os.environ['HADOOP_HOME'])
print('  ✅ SPARK_LOCAL_DIRS:', os.environ['SPARK_LOCAL_DIRS'])
print()

# Step 2: Import PySpark
print('Step 2: Importing PySpark...')
try:
    from pyspark.sql import SparkSession
    print('  ✅ PySpark imported successfully')
    print()
except Exception as e:
    print('  ❌ Failed:', e)
    sys.exit(1)

# Step 3: Create simple Spark session
print('Step 3: Creating Spark session...')
try:
    spark = SparkSession.builder \
        .appName('BasicTest') \
        .master('local[1]') \
        .config('spark.driver.host', 'localhost') \
        .config('spark.driver.bindAddress', '127.0.0.1') \
        .config('spark.sql.warehouse.dir', 'file:///C:/tmp/spark-warehouse') \
        .config('spark.ui.enabled', 'false') \
        .getOrCreate()
    
    print('  ✅ Spark session created!')
    print('  Version:', spark.version)
    print()
except Exception as e:
    print('  ❌ Failed to create Spark session')
    print('  Error:', str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Test basic DataFrame
print('Step 4: Testing basic DataFrame operations...')
try:
    data = [('Alice', 25), ('Bob', 30), ('Charlie', 35)]
    df = spark.createDataFrame(data, ['name', 'age'])
    
    print('  ✅ DataFrame created')
    print()
    print('  Data:')
    df.show()
    print()
    
    # Test aggregation
    avg_age = df.agg({'age': 'avg'}).collect()[0][0]
    print(f'  Average age: {avg_age}')
    print('  ✅ Aggregation works')
    print()
    
except Exception as e:
    print('  ❌ DataFrame test failed:', e)
    spark.stop()
    sys.exit(1)

# Step 5: Success!
print('=' * 80)
print('✅ ALL TESTS PASSED!')
print('Spark is working correctly!')
print('=' * 80)

spark.stop()