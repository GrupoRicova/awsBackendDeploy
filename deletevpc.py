import boto3
from dotenv import load_dotenv
import os

# Load environment variables from .env file

def delete_all_vpcs():
    # Create a Boto3 client for EC2
    load_dotenv()

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = 'us-east-1'  # Replace with your desired region

# Create a Boto3 client for EC2 with explicit credentials
    ec2_client = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)


    # Retrieve all VPCs in the account
    response = ec2_client.describe_vpcs()

    # Extract the VPC IDs from the response
    vpc_ids = [vpc['VpcId'] for vpc in response['Vpcs']]

    # Delete each VPC
    for vpc_id in vpc_ids:
        # Delete any attached internet gateways
        response = ec2_client.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}])
        for igw in response['InternetGateways']:
            igw_id = igw['InternetGatewayId']
            ec2_client.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
            ec2_client.delete_internet_gateway(InternetGatewayId=igw_id)

        # Delete any attached NAT gateways
        response = ec2_client.describe_nat_gateways(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        for nat_gateway in response['NatGateways']:
            nat_gateway_id = nat_gateway['NatGatewayId']
            ec2_client.delete_nat_gateway(NatGatewayId=nat_gateway_id)

        # Delete any attached VPC endpoints
        response = ec2_client.describe_vpc_endpoints(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        for vpc_endpoint in response['VpcEndpoints']:
            vpc_endpoint_id = vpc_endpoint['VpcEndpointId']
            ec2_client.delete_vpc_endpoints(VpcEndpointIds=[vpc_endpoint_id])

        # Delete any attached VPC peering connections
        response = ec2_client.describe_vpc_peering_connections(Filters=[{'Name': 'accepter-vpc-info.vpc-id', 'Values': [vpc_id]}])
        for vpc_peering_connection in response['VpcPeeringConnections']:
            vpc_peering_connection_id = vpc_peering_connection['VpcPeeringConnectionId']
            ec2_client.delete_vpc_peering_connection(VpcPeeringConnectionId=vpc_peering_connection_id)

        # Delete any attached security groups
        response = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        for security_group in response['SecurityGroups']:
            security_group_id = security_group['GroupId']
            ec2_client.delete_security_group(GroupId=security_group_id)

        # Delete the VPC
        ec2_client.delete_vpc(VpcId=vpc_id)

    print('All VPCs deleted successfully!')

# Call the function to delete all VPCs
delete_all_vpcs()
