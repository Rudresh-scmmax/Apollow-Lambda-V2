"""
Deployment script for the price forecasting Lambda function
"""
import boto3
import zipfile
import os
import json
from pathlib import Path

def create_deployment_package():
    """Create a deployment package for the Lambda function"""
    
    # Create a temporary directory for the package
    package_dir = "lambda_package"
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy the main handler
    os.system(f"copy lambda_handler.py {package_dir}\\")
    
    # Copy the database query module
    os.system(f"copy ..\\Pdf_Processor\\db_query.py {package_dir}\\")
    
    # Install dependencies
    os.system(f"pip install -r requirements.txt -t {package_dir}\\")
    
    # Create zip file
    with zipfile.ZipFile("price_forecast_lambda.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_path)
    
    print("Deployment package created: price_forecast_lambda.zip")
    return "price_forecast_lambda.zip"

def deploy_lambda():
    """Deploy the Lambda function to AWS"""
    
    # Create deployment package
    zip_file = create_deployment_package()
    
    # Initialize AWS clients
    lambda_client = boto3.client('lambda')
    iam_client = boto3.client('iam')
    
    # Function configuration
    function_name = "price-forecast-lambda"
    role_name = "price-forecast-lambda-role"
    
    try:
        # Create IAM role for Lambda
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        try:
            role = iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description="Role for price forecast Lambda function"
            )
            role_arn = role['Role']['Arn']
        except iam_client.exceptions.EntityAlreadyExistsException:
            # Role already exists, get its ARN
            role_arn = f"arn:aws:iam::{boto3.client('sts').get_caller_identity()['Account']}:role/{role_name}"
        
        # Attach basic execution policy
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        )
        
        # Attach additional policies for database access
        additional_policies = [
            "arn:aws:iam::aws:policy/AmazonRDSFullAccess",
            "arn:aws:iam::aws:policy/AmazonVPCFullAccess"
        ]
        
        for policy_arn in additional_policies:
            try:
                iam_client.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_arn
                )
            except Exception as e:
                print(f"Warning: Could not attach policy {policy_arn}: {e}")
        
        # Wait for role to be ready
        import time
        time.sleep(10)
        
        # Read the zip file
        with open(zip_file, 'rb') as f:
            zip_content = f.read()
        
        # Create or update Lambda function
        try:
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.11',
                Role=role_arn,
                Handler='lambda_handler.lambda_handler',
                Code={'ZipFile': zip_content},
                Description='Price forecasting Lambda function',
                Timeout=300,  # 5 minutes
                MemorySize=1024,  # 1GB
                Environment={
                    'Variables': {
                        'PYTHONPATH': '/var/task'
                    }
                }
            )
            print(f"Lambda function created: {function_name}")
            
        except lambda_client.exceptions.ResourceConflictException:
            # Function already exists, update it
            response = lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )
            print(f"Lambda function updated: {function_name}")
        
        print(f"Function ARN: {response['FunctionArn']}")
        
        # Clean up
        os.remove(zip_file)
        import shutil
        shutil.rmtree("lambda_package", ignore_errors=True)
        
        return response['FunctionArn']
        
    except Exception as e:
        print(f"Error deploying Lambda function: {e}")
        return None

if __name__ == "__main__":
    print("Deploying price forecasting Lambda function...")
    function_arn = deploy_lambda()
    if function_arn:
        print(f"Deployment successful! Function ARN: {function_arn}")
    else:
        print("Deployment failed!")
