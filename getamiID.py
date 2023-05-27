import boto3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = 'us-west-2'  # Replace with your desired region

# Create a Boto3 client for EC2 with explicit credentials
ec2_client = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)


response = ec2_client.describe_images(
    Filters=[
        {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-focal-22.04-amd64-server-*']},
        {'Name': 'architecture', 'Values': ['x86_64']},
        {'Name': 'state', 'Values': ['available']},
    ],
    Owners=['099720109477']  # Canonical owner ID
)

images = response['Images']
images.sort(key=lambda x: x['CreationDate'], reverse=True)

if images:
    latest_ubuntu_2204_ami_id = images[0]['ImageId']
    print("Latest Ubuntu Server 22.04 LTS AMI ID:", latest_ubuntu_2204_ami_id)
else:
    print("No matching AMI found.")
