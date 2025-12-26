"""
Test AWS connection and permissions
"""

import boto3
from botocore.exceptions import ClientError

def test_aws_connection():
    print('Testing AWS Connection...')
    print('=' * 60)
    
    try:
        # Test STS (authentication)
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        account = identity['Account']
        user_arn = identity['Arn']
        
        print('AWS Authentication Successful!')
        print(f'   Account: {account}')
        print(f'   User: {user_arn}')
        print()
        
        # Test S3
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        bucket_list = buckets['Buckets']
        
        print('S3 Access Working!')
        print(f'   Buckets found: {len(bucket_list)}')
        for bucket in bucket_list:
            bucket_name = bucket['Name']
            print(f'   - {bucket_name}')
        print()
        
        # Test Kinesis
        kinesis = boto3.client('kinesis')
        streams = kinesis.list_streams()
        stream_names = streams['StreamNames']
        
        print('Kinesis Access Working!')
        print(f'   Streams found: {len(stream_names)}')
        for stream in stream_names:
            print(f'   - {stream}')
        print()
        
        print('=' * 60)
        print('All AWS services accessible!')
        print('=' * 60)
        
        return True
        
    except ClientError as e:
        print(f'AWS Error: {e}')
        return False
    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == '__main__':
    success = test_aws_connection()
    if success:
        print('\nYou are ready to use AWS services!')
    else:
        print('\nPlease check your AWS credentials and permissions.')
