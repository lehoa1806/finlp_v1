---
# Project
project: 'finlp'
project_code: 'https://github.com/lehoa1806/finlp.git'
project_home: '/home/ubuntu/finlp'
project_branch: 'main'

# User
user_name: 'ubuntu'

# Account info
aws_region: 'ap-southeast-1'
aws_account_id: {{ grains.aws_account_id }}

# Network
vpc:
  vpc_id: {{ grains.vpc_id }}

# API GATEWAY
api_gateway_stage: prod
api_key_required: false
authorization_type: 'NONE'
error_response_template:
  '"#set($errorMessage = $input.path(\"$.errorMessage\"))
  \n{\n\   \"message\": \"$errorMessage\"\n}\n"'
lambda_name_format: '"{api}_{resource}_{method}"'
response_template: '"$input.json(\"$\")\n"'

# IAM
iam_version: 2012-10-17
iam_api_gateway_role: user-api-gateway-{{ grains.aws_account_id }}
iam_ec2_role: developer-ec2-{{ grains.aws_account_id }}
iam_lambda_role: user-lambda-{{ grains.aws_account_id }}

# Lambda
lambda_description: Lambda function of FinLP
lambda_s3_object: codebase-latest.zip
lambda_runtime: python3.8
lambda_timeout: 60
lambda_memory: 128

# S3
s3_news_bucket: finulp-news
s3_secret_bucket: finulp-secrets
s3_workspace_bucket: finulp-workspace
