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
iam_ec2_role: developer-ec2-{{ grains.aws_account_id }}

# Network
vpc:
  vpc_id: {{ grains.vpc_id }}
