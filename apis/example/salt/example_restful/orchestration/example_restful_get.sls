---
include:
  - iam_lambda_role

create {{ pillar.example_restful_get_lambda_name }} lambda:
  boto_lambda.function_present:
    - FunctionName: {{ pillar.example_restful_get_lambda_name }}
    - Runtime: {{ pillar.lambda_runtime }}
    - Role: {{ pillar.iam_lambda_role }}
    - Handler: {{ pillar.example_restful_get_lambda_handler }}
    - S3Bucket: {{ pillar.s3_workspace_bucket }}
    - S3Key: {{ pillar.lambda_s3_object }}
    - Description: {{ pillar.example_restful_get_lambda_description }}
    - Timeout: {{ pillar.lambda_timeout }}
    - MemorySize: {{ pillar.lambda_memory }}
    - region: {{ pillar.aws_region }}
