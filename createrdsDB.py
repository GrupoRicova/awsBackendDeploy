import boto3

# Specify your AWS credentials and region
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = 'us-west-2'  # Replace with your desired region

# Create a Boto3 client for RDS with explicit credentials
rds_client = boto3.client('rds', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Specify the RDS instance details
db_instance_identifier = 'strapi-database'
db_instance_class = 'db.m6g.4xlarge'
engine = 'postgres'
engine_version =  "15.3"
master_username = 'ricova'
master_password = 'GrupoRicova2023'
allocated_storage = 20
db_name = 'strapiRicova'

# Create the RDS instance
response = rds_client.create_db_instance(
    DBInstanceIdentifier=db_instance_identifier,
    DBInstanceClass=db_instance_class,
    Engine=engine,
    EngineVersion=engine_version,
    MasterUsername=master_username,
    MasterUserPassword=master_password,
    AllocatedStorage=allocated_storage,
    DBName=db_name,
    PubliclyAccessible=True,  # Set to False if you want the instance to be accessible only within the VPC
    MultiAZ=False,  # Set to True if you want a Multi-AZ deployment
    StorageType='gp2',  # Change storage type as per your requirements
    Tags=[
        {'Key': 'Name', 'Value': 'strapiDatabaseRicova'},  # Replace with your desired name
    ],
)

print('Database creation in progress...')
