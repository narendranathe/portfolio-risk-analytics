# 🔧 Troubleshooting Guide

## Project Development Roadblocks & Solutions

This document chronicles the technical challenges encountered during development and how they were resolved.

---

## 1. AWS Kinesis Setup

### Problem: IAM Permission Issues
**Error:** `AccessDeniedException` when accessing Kinesis streams

**Root Cause:** IAM user lacked proper Kinesis permissions

**Solution:**
```bash
# AWS Console → IAM → Users → Attach policies
# Added: AmazonKinesisFullAccess

# Waited 30 seconds for permission propagation
```

**Lesson:** IAM users cannot modify their own permissions via CLI (correct security practice)

---

## 2. Kafka Import Conflicts

### Problem: Module Import Error
**Error:** `ImportError: cannot import name 'KafkaProducer' from 'kafka'`

**Root Cause:** Local folder `src/streaming/kafka/` conflicted with `kafka-python` package

**Python's import order:**
1. Current directory/subdirectories ← Found local `kafka/` folder
2. Installed packages ← Never reached `kafka-python`

**Solution:**
```bash
# Deleted local kafka/ subfolder
rmdir /s src\streaming\kafka

# Kept files directly in src/streaming/:
# - kafka_producer.py
# - kafka_consumer_simple.py
```

**Lesson:** Never name local folders the same as installed packages

---

## 3. Spark on Windows - Multiple Issues

### Issue 3.1: Hadoop Winutils Missing

**Error:** `The system cannot find the path specified`

**Root Cause:** Spark requires Hadoop binaries even on Windows

**Solution:**
```bash
# Download winutils and hadoop.dll
curl -L https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.5/bin/winutils.exe -o C:\hadoop\bin\winutils.exe
curl -L https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.5/bin/hadoop.dll -o C:\hadoop\bin\hadoop.dll

# Set HADOOP_HOME
setx HADOOP_HOME "C:\hadoop" /M
```

**Files Required:**
- `winutils.exe` (~112 KB)
- `hadoop.dll` (~85 KB)

---

### Issue 3.2: Java Not Found

**Error:** `FileNotFoundError: [WinError 2] The system cannot find the file specified`

**Root Cause:** Spark couldn't locate Java executable

**Solution:**
```python
# Set JAVA_HOME in Python before importing PySpark
import os
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-11'

# Verify Java path
import subprocess
subprocess.run(['java', '-version'])
```

**Verification:**
```bash
java -version
# Output: java version "11.0.29"
```

---

### Issue 3.3: Python Worker Failed to Connect

**Error:** `Python worker failed to connect back`

**Most Critical Issue** - Even after Java and Hadoop were configured

**Root Cause:** Spark couldn't find Python to launch worker processes

**Solution:**
```python
import sys
import os

# CRITICAL: Tell Spark which Python to use
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# Example output:
# sys.executable = 'C:\\Users\\naren\\anaconda3\\envs\\portfolio-risk\\python.exe'
```

**Why This Worked:**
- Spark tries to launch Python workers using system PATH
- Windows has Microsoft Store Python stub that doesn't work
- Explicitly setting Python path bypasses PATH search
- Uses Anaconda environment Python directly

---

## 4. PowerShell vs CMD Differences

### Problem: File Creation Syntax Errors

**Error:** `type nul > file` worked in CMD but not PowerShell

**Solution:**
```powershell
# PowerShell equivalents:
New-Item -ItemType File -Path "filename"
Out-File -FilePath "filename" -Encoding utf8
```

**Issue with Multi-line Commands:**
- PowerShell requires different syntax for environment variables
- Used Python scripts for complex file creation

---

## 5. F-String Escaping Issues

### Problem: Docstring Backslash Errors

**Error:** `SyntaxError: unexpected character after line continuation character`

**Root Cause:** Escaped quotes in f-strings: `f"{data['key']}"`

**Solution:**
```python
# WRONG (causes errors in PowerShell file creation):
f'{data["symbol"]}: ${data["price"]:.2f}'

# CORRECT - Use .format():
'{}: ${:.2f}'.format(data['symbol'], data['price'])
```

---

## 6. Environment Variable Concatenation

### Problem: Variables Mashed Together

**Error:**
```bash
echo %HADOOP_HOME%
# Output: C:\hadoopset SPARK_LOCAL_DIRS=C:\tmpset JAVA_HOME=...
```

**Root Cause:** Set commands on same line without separation

**Solution:**
```bash
# Set ONE AT A TIME (each on separate line):
set HADOOP_HOME=C:\hadoop
set SPARK_LOCAL_DIRS=C:\tmp
set JAVA_HOME=C:\Program Files\Java\jdk-11
```

---

## 7. Spark Checkpoint Directory Permissions

### Problem: Temporary checkpoint errors

**Warning:** `Temporary checkpoint location created which is deleted...`

**Solution:**
```bash
# Create permanent directories:
mkdir C:\tmp\checkpoints
mkdir C:\tmp\spark-warehouse
mkdir C:\tmp\spark-events

# Set permissions:
icacls C:\tmp /grant Everyone:F /T
```

---

## Complete Working Environment Setup

### Final Environment Variables (Set in Python)
```python
import os
import sys

# Spark Python configuration
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# Hadoop configuration
os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['SPARK_LOCAL_DIRS'] = r'C:\tmp'

# Java configuration
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-11'
```

### Directory Structure Created
```
C:\
├── hadoop\
│   └── bin\
│       ├── winutils.exe
│       └── hadoop.dll
│
└── tmp\
    ├── checkpoints\
    ├── spark-warehouse\
    ├── spark-events\
    └── hive\
```

---

## Key Takeaways

### What Worked
1. ✅ Setting Python path BEFORE importing PySpark
2. ✅ Using absolute paths for all configuration
3. ✅ Creating directories with proper permissions
4. ✅ Downloading correct Hadoop version (3.3.5)
5. ✅ Using conda environment Python explicitly

### What Didn't Work
1. ❌ Relying on system PATH for Python
2. ❌ Using relative paths for checkpoints
3. ❌ Assuming Spark works out-of-box on Windows
4. ❌ Setting environment variables in shell vs Python
5. ❌ Using f-strings with backslashes in shell scripts

### Time Investment
- Kafka setup: ~30 minutes
- Spark basic setup: ~2 hours (multiple iterations)
- Python worker issue: ~1 hour (critical fix)
- Total debugging time: ~3.5 hours

### Was It Worth It?
**YES!** Now we have:
- Production-grade Spark Structured Streaming
- Real-time windowed aggregations
- Kafka + Spark integration
- Knowledge of Windows + Spark quirks
- Reusable setup for future projects

---

## Quick Reference: Working Spark Kafka Consumer
```python
#!/usr/bin/env python
"""Production Spark Kafka Consumer"""

import os
import sys

# CRITICAL: Set before importing PySpark
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-11'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName('KafkaConsumer') \
    .master('local[2]') \
    .config('spark.jars.packages', 
            'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
    .getOrCreate()

# Read from Kafka and process...
```

---

## Resources Used

- **Hadoop Winutils:** https://github.com/cdarlint/winutils
- **PySpark Docs:** https://spark.apache.org/docs/latest/api/python/
- **Kafka Python:** https://kafka-python.readthedocs.io/
- **Stack Overflow:** Various Windows + Spark issues

---

## Future Developers

If you're setting up this project on Windows:

1. Read this document FIRST
2. Run `scripts/test_spark.py` to verify setup
3. Check all environment variables are set
4. Ensure Java 11+ is installed
5. Download Hadoop winutils before starting

**Don't skip the environment setup** - it saves hours of debugging!