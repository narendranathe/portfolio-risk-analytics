"""
Spark test with Java path properly set
"""

import os
import sys
import subprocess

print('=' * 80)
print('SPARK WITH JAVA PATH FIX')
print('=' * 80)
print()

# Step 1: Find Java
print('Step 1: Locating Java...')

# Check if java is in PATH
try:
    result = subprocess.run(['java', '-version'], capture_output=True, text=True)
    print('  ✅ Java found in PATH')
    print('  Version:', result.stderr.split('\n')[0])
except Exception as e:
    print('  ❌ Java not in PATH:', e)

# Set JAVA_HOME
java_home = r'C:\Program Files\Java\jdk-11.0.21'

if os.path.exists(java_home):
    print(f'  ✅ JAVA_HOME found: {java_home}')
    os.environ['JAVA_HOME'] = java_home
    
    # Add Java bin to PATH
    java_bin = os.path.join(java_home, 'bin')
    os.environ['PATH'] = java_bin + os.pathsep + os.environ.get('PATH', '')
    print(f'  ✅ Added to PATH: {java_bin}')
else:
    print(f'  ❌ JAVA_HOME not found at: {java_home}')
    # Try to find Java
    possible_paths = [
        r'C:\Program Files\Java\jdk-17',
        r'C:\Program Files\Java\jdk-11',
        r'C:\Program Files\Java\jre-11',
    ]
    for path in possible_paths:
        if os.path.exists(path):
            java_home = path
            os.environ['JAVA_HOME'] = path
            print(f'  ✅ Found Java at: {path}')
            break

print()

# Step 2: Set Hadoop
print('Step 2: Setting Hadoop...')
os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['SPARK_LOCAL_DIRS'] = r'C:\tmp'
print('  ✅ HADOOP_HOME:', os.environ['HADOOP_HOME'])
print('  ✅ SPARK_LOCAL_DIRS:', os.environ['SPARK_LOCAL_DIRS'])
print()

# Step 3: Verify environment
print('Step 3: Verifying environment...')
print('  JAVA_HOME:', os.environ.get('JAVA_HOME', 'NOT SET'))
print('  HADOOP_HOME:', os.environ.get('HADOOP_HOME', 'NOT SET'))
print()

# Step 4: Import and create Spark
print('Step 4: Creating Spark session...')

try:
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder \
        .appName('JavaPathTest') \
        .master('local[1]') \
        .config('spark.driver.host', '127.0.0.1') \
        .config('spark.driver.bindAddress', '127.0.0.1') \
        .config('spark.sql.warehouse.dir', 'file:///C:/tmp/spark-warehouse') \
        .config('spark.ui.enabled', 'false') \
        .getOrCreate()
    
    print('  ✅ Spark session created!')
    print('  Version:', spark.version)
    print()
    
    # Test
    print('Step 5: Testing...')
    data = [('Alice', 25), ('Bob', 30)]
    df = spark.createDataFrame(data, ['name', 'age'])
    df.show()
    
    print('  ✅ Test successful!')
    
    spark.stop()
    
    print()
    print('=' * 80)
    print('✅ SUCCESS! SPARK IS WORKING!')
    print('=' * 80)
    
except Exception as e:
    print('  ❌ Failed:', e)
    import traceback
    traceback.print_exc()
    sys.exit(1)