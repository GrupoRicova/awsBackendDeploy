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

# Specify the instance details
image_id = "ami-0c65adc9a5c1b5d7c"  # Replace with the appropriate AMI ID for Ubuntu Server 22.04 LTS
instance_type = 't2.micro'
key_name = 'ricovakeyP'  # Replace with the name of your key pair
security_group_name = 'ricovagroupforStrapi'
security_group_description = 'strapi instance security settings'
security_group_rules = [
    {
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
        'Ipv6Ranges': [{'CidrIpv6': '::/0'}],
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 80,
        'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
        'Ipv6Ranges': [{'CidrIpv6': '::/0'}],
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 443,
        'ToPort': 443,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
        'Ipv6Ranges': [{'CidrIpv6': '::/0'}],
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 1337,
        'ToPort': 1337,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
        'Ipv6Ranges': [{'CidrIpv6': '::/0'}],
    }
]

# Create the security group
response = ec2_client.create_security_group(
    Description=security_group_description,
    GroupName=security_group_name,
)
security_group_id = response['GroupId']

# Authorize the security group rules
for rule in security_group_rules:
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[{
            'IpProtocol': rule['IpProtocol'],
            'FromPort': rule['FromPort'],
            'ToPort': rule['ToPort'],
            'IpRanges': rule['IpRanges'],
            'Ipv6Ranges': rule['Ipv6Ranges'],
        }],
    )

# Launch the EC2 instance
response = ec2_client.run_instances(
    ImageId=image_id,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    KeyName=key_name,
    SecurityGroupIds=[security_group_id],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'strapi-instance'}  # Replace with your desired name
            ]
        }
    ],
    UserData='#!/bin/bash\n\n# Add your custom user data here',
    Monitoring={'Enabled': False}  # Change to True if you want instance monitoring enabled
)

instance_id = response['Instances'][0]['InstanceId']
print('Instance launched successfully!')
print('Instance ID:', instance_id)
