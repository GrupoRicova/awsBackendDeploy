import boto3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = 'us-east-1'  # Replace with your desired region

# Create a Boto3 client for EC2 with explicit credentials
ec2_client = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Specify the key pair name
key_pair_name = 'ricovakey'

# Create the key pair
response = ec2_client.create_key_pair(KeyName=key_pair_name)

# Retrieve the private key
private_key = response['KeyMaterial']

# Save the private key to a file
with open(key_pair_name+'.pem', 'w') as f:
    f.write(private_key)

# Set appropriate permissions for the private key file
import os
os.chmod(key_pair_name+'.pem', 0o400)

# Display success message
print(f'Key pair "{key_pair_name}" created and private key saved to my-key-pair.pem')
