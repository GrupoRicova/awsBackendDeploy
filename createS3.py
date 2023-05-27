import boto3

from dotenv import load_dotenv
import os
import json 
# Load environment variables from .env file
load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = 'us-west-2'  # Replace with your desired region

# Create a Boto3 client for RDS with explicit credentials

s3 = boto3.client('s3', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# 1. Create the bucket
bucket_name = 'ricova-project-strapi-prod'


"""s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': region
    }
)"""


waiter = s3.get_waiter('bucket_exists')

# Wait until the bucket exists
waiter.wait(Bucket=bucket_name)

# 2. Configure bucket permissions
bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [
        {
            'Sid': 'PublicReadGetObject',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': 's3:GetObject',
            'Resource': f'arn:aws:s3:::{bucket_name}/*'
        }
    ]
}
bucket_policy = json.dumps(bucket_policy)
print(bucket_policy)
s3.put_bucket_policy(
    Bucket=bucket_name,
    Policy=bucket_policy
)

# Enable versioning for the bucket (optional)
s3.put_bucket_versioning(
    Bucket=bucket_name,
    VersioningConfiguration={
        'Status': 'Enabled'
    }
)

# Disable public access block (optional)
s3.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': False,
        'IgnorePublicAcls': False,
        'BlockPublicPolicy': False,
        'RestrictPublicBuckets': False
    }
)
print('Bucket created and configured successfully.')
