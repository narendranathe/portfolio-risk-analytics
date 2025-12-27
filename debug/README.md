# Debug & Testing Files

This folder contains all diagnostic and test files used during development to troubleshoot various issues.

## Files

### Spark Diagnostics
- `test_spark_basic.py` - Basic Spark session test
- `test_spark_detailed.py` - Detailed error logging
- `test_spark_with_java.py` - Java path testing
- `spark_working_final.py` - Final working Spark test
- `spark_kafka_final.py` - Kafka integration test

### Working Versions
- `../scripts/test_spark.py` - Production Spark test
- `../src/streaming/spark_kafka_consumer.py` - Production Kafka consumer

## Usage

These files were used to diagnose and fix:
- Windows + Spark compatibility issues
- Python worker path problems
- Hadoop winutils configuration
- Java/Kafka integration

See `../TROUBLESHOOTING.md` for detailed problem-solving documentation.