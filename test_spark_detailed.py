"""
Detailed Spark test with full error logging
"""

import os
import sys
import traceback

print('=' * 80)
print('DETAILED SPARK DIAGNOSTIC')
print('=' * 80)
print()

# Step 1: Set environment
print('Step 1: Setting environment...')
os.environ['HADOOP_HOME'] = 'C:\\hadoop'
os.environ['SPARK_LOCAL_DIRS'] = 'C:\\tmp'
os.environ['SPARK_HOME'] = 'C:\\tmp\\spark'
print('  ✅ Environment variables set')
print()

# Step 2: Create all necessary directories
print('Step 2: Creating directories...')
directories = [
    'C:\\tmp',
    'C:\\tmp\\hive',
    'C:\\tmp\\spark-events',
    'C:\\tmp\\spark-warehouse',
    'C:\\tmp\\checkpoints',
    'C:\\hadoop\\tmp'
]

for directory in directories:
    try:
        os.makedirs(directory, exist_ok=True)
        print(f'  ✅ {directory}')
    except Exception as e:
        print(f'  ❌ {directory}: {e}')

print()

# Step 3: Verify files exist
print('Step 3: Verifying Hadoop binaries...')
winutils = 'C:\\hadoop\\bin\\winutils.exe'
hadoop_dll = 'C:\\hadoop\\bin\\hadoop.dll'

if os.path.exists(winutils):
    size = os.path.getsize(winutils)
    print(f'  ✅ winutils.exe ({size:,} bytes)')
else:
    print(f'  ❌ winutils.exe NOT FOUND')

if os.path.exists(hadoop_dll):
    size = os.path.getsize(hadoop_dll)
    print(f'  ✅ hadoop.dll ({size:,} bytes)')
else:
    print(f'  ❌ hadoop.dll NOT FOUND')

print()

# Step 4: Import PySpark
print('Step 4: Importing PySpark...')
try:
    from pyspark.sql import SparkSession
    from pyspark import SparkConf
    print('  ✅ PySpark imported')
    print()
except Exception as e:
    print(f'  ❌ Import failed: {e}')
    sys.exit(1)

# Step 5: Create Spark session with DETAILED error catching
print('Step 5: Creating Spark session...')
print('  (This is where the error happens)')
print()

try:
    # Create configuration first
    conf = SparkConf()
    conf.setAppName('DetailedTest')
    conf.setMaster('local[1]')
    conf.set('spark.driver.host', '127.0.0.1')
    conf.set('spark.driver.bindAddress', '127.0.0.1')
    conf.set('spark.sql.warehouse.dir', 'file:///C:/tmp/spark-warehouse')
    conf.set('spark.local.dir', 'C:/tmp')
    conf.set('spark.driver.extraJavaOptions', '-Djava.io.tmpdir=C:/tmp')
    conf.set('spark.executor.extraJavaOptions', '-Djava.io.tmpdir=C:/tmp')
    conf.set('spark.ui.enabled', 'false')
    
    print('  Configuration created')
    print('  Attempting to create session...')
    
    # Create session
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    
    print('  ✅ Spark session created!')
    print(f'  Version: {spark.version}')
    print()
    
    # Test it
    print('Step 6: Testing basic operation...')
    data = [('test', 1)]
    df = spark.createDataFrame(data, ['name', 'value'])
    df.show()
    print('  ✅ Test successful!')
    
    spark.stop()
    print()
    print('=' * 80)
    print('✅ ALL TESTS PASSED!')
    print('=' * 80)
    
except Exception as e:
    print()
    print('❌ DETAILED ERROR INFORMATION:')
    print('=' * 80)
    print('Error type:', type(e).__name__)
    print('Error message:', str(e))
    print()
    print('Full traceback:')
    print('-' * 80)
    traceback.print_exc()
    print('=' * 80)
    sys.exit(1)