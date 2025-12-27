"""
Diagnostic Spark Test
"""

import os
import sys

print('=' * 80)
print('SPARK DIAGNOSTIC TEST')
print('=' * 80)
print()

# Check environment
print('1. Python Version:', sys.version)
print('2. Current Directory:', os.getcwd())
print('3. HADOOP_HOME:', os.environ.get('HADOOP_HOME', 'NOT SET'))
print('4. JAVA_HOME:', os.environ.get('JAVA_HOME', 'NOT SET'))
print()

# Try importing PySpark
print('5. Importing PySpark...')
try:
    import pyspark
    print('   ✅ PySpark version:', pyspark.__version__)
except Exception as e:
    print('   ❌ Error:', e)
    sys.exit(1)

print()
print('6. Creating Spark Session...')
try:
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder \
        .appName('DiagnosticTest') \
        .master('local[1]') \
        .getOrCreate()
    
    print('   ✅ Spark session created!')
    print('   Spark version:', spark.version)
    
    # Try simple operation
    print()
    print('7. Testing simple operation...')
    data = [('Alice', 1), ('Bob', 2)]
    df = spark.createDataFrame(data, ['name', 'value'])
    df.show()
    
    print('   ✅ Spark is working!')
    
    spark.stop()
    
except Exception as e:
    print('   ❌ Error:', e)
    import traceback
    traceback.print_exc()

print()
print('=' * 80)
print('DIAGNOSTIC COMPLETE')
print('=' * 80)