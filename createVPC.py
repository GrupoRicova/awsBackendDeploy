import boto3
import csv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = 'us-east-1'  # Replace with your desired region

# Create a Boto3 client for EC2 with explicit credentials
ec2_client = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Create the VPC
response = ec2_client.create_vpc(
    CidrBlock='10.0.0.0/16',
    InstanceTenancy='default'
)

vpc_id = response['Vpc']['VpcId']

# Wait until the VPC is available
ec2_client.get_waiter('vpc_available').wait(VpcIds=[vpc_id])

# Add tags to the VPC
ec2_client.create_tags(
    Resources=[vpc_id],
    Tags=[
        {'Key': 'Name', 'Value': 'strapi-vpc'},  # Replace with your desired name
    ]
)

# Enable DNS hostnames
ec2_client.modify_vpc_attribute(
    VpcId=vpc_id,
    EnableDnsHostnames={'Value': True}
)

# Enable DNS support
ec2_client.modify_vpc_attribute(
    VpcId=vpc_id,
    EnableDnsSupport={'Value': True}
)

# Create two public subnets
public_subnet_response = ec2_client.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.1.0/24',  # Replace with your desired CIDR block
    AvailabilityZone=region + 'a'  # Replace with the appropriate availability zone
)

public_subnet_id = public_subnet_response['Subnet']['SubnetId']

# Retrieve the public subnet's route table ID
public_route_table_response = ec2_client.describe_route_tables(
    Filters=[
        {'Name': 'association.subnet-id', 'Values': [public_subnet_id]}
    ]
)

public_route_table_id = public_route_table_response['RouteTables'][0]['RouteTableId']

# Create two private subnets
private_subnet_response = ec2_client.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.2.0/24',  # Replace with your desired CIDR block
    AvailabilityZone=region + 'b'  # Replace with the appropriate availability zone
)

private_subnet_id = private_subnet_response['Subnet']['SubnetId']

# Create the VPC endpoint for S3
ec2_client.create_vpc_endpoint(
    VpcId=vpc_id,
    ServiceName='com.amazonaws.' + region + '.s3',
    RouteTableIds=[public_route_table_id],  # Pass the public subnet's route table ID
)

# Write VPC details to CSV file
csv_file = 'vpc_details.csv'

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['VPC ID', 'Public Subnet ID', 'Private Subnet ID'])
    writer.writerow([vpc_id, public_subnet_id, private_subnet_id])

print('VPC created successfully!')
print('VPC ID:', vpc_id)
print('Public Subnet ID:', public_subnet_id)
print('Private Subnet ID:', private_subnet_id)
print('VPC details written to', csv_file)
