"""
Spark with Python path fix - FINAL VERSION
"""

import os
import sys
import subprocess

print('=' * 80)
print('SPARK - FINAL FIX')
print('=' * 80)
print()

# Step 1: Find Python executable
python_exe = sys.executable
print('Step 1: Python executable')
print('  Path:', python_exe)
print('  Version:', sys.version.split()[0])
print()

# Step 2: Set environment for Spark
print('Step 2: Setting environment...')
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-11'
os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['SPARK_LOCAL_DIRS'] = r'C:\tmp'

# CRITICAL: Tell Spark which Python to use
os.environ['PYSPARK_PYTHON'] = python_exe
os.environ['PYSPARK_DRIVER_PYTHON'] = python_exe

print('  ✅ JAVA_HOME:', os.environ['JAVA_HOME'])
print('  ✅ HADOOP_HOME:', os.environ['HADOOP_HOME'])
print('  ✅ PYSPARK_PYTHON:', os.environ['PYSPARK_PYTHON'])
print()

# Step 3: Create Spark session
print('Step 3: Creating Spark session...')

from pyspark.sql import SparkSession

try:
    spark = SparkSession.builder \
        .appName('FinalTest') \
        .master('local[2]') \
        .config('spark.driver.host', '127.0.0.1') \
        .config('spark.driver.bindAddress', '127.0.0.1') \
        .config('spark.sql.warehouse.dir', 'file:///C:/tmp/spark-warehouse') \
        .config('spark.ui.enabled', 'false') \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel('ERROR')
    
    print('  ✅ Spark session created!')
    print('  Version:', spark.version)
    print()
    
    # Step 4: TEST with actual DataFrame
    print('Step 4: Testing DataFrame operations...')
    
    data = [
        ('Alice', 25, 'Engineering'),
        ('Bob', 30, 'Sales'),
        ('Charlie', 35, 'Marketing'),
        ('Diana', 28, 'Engineering'),
        ('Eve', 32, 'Sales')
    ]
    
    df = spark.createDataFrame(data, ['name', 'age', 'department'])
    
    print('  Created DataFrame:')
    df.show()
    
    print('  Department count:')
    df.groupBy('department').count().show()
    
    print('  Average age by department:')
    df.groupBy('department').avg('age').show()
    
    print()
    print('=' * 80)
    print('✅ SUCCESS! SPARK IS FULLY WORKING!')
    print('=' * 80)
    
    spark.stop()
    
except Exception as e:
    print('  ❌ Error:', e)
    import traceback
    traceback.print_exc()
    sys.exit(1)