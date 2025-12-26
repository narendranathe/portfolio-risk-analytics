"""
Verify complete environment setup
"""

import sys

def check_package(package_name):
    try:
        __import__(package_name)
        print(f'✅ {package_name} installed')
        return True
    except ImportError:
        print(f'❌ {package_name} NOT installed')
        return False

def main():
    print('=' * 60)
    print('ENVIRONMENT SETUP VERIFICATION')
    print('=' * 60)
    print()
    
    # Check Python version
    print(f'Python version: {sys.version}')
    print()
    
    # Check required packages
    packages = [
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'boto3',
        'botocore',
        'yfinance',
        'scipy'
    ]
    
    print('Checking packages:')
    all_installed = True
    for package in packages:
        if not check_package(package):
            all_installed = False
    
    print()
    print('=' * 60)
    
    if all_installed:
        print('🎉 All packages installed correctly!')
        print()
        print('Next steps:')
        print('1. Configure AWS: aws configure')
        print('2. Test AWS: python scripts\\test_aws_connection.py')
        print('3. Run market simulator: python src\\data_ingestion\\market_data_simulator.py')
    else:
        print('⚠️  Some packages missing!')
        print()
        print('Install missing packages with:')
        print('pip install boto3 numpy pandas matplotlib seaborn yfinance scipy')
    
    print('=' * 60)

if __name__ == '__main__':
    main()
