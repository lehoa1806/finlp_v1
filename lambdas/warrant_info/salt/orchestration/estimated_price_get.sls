---
Ensure {{ pillar.estimated_price_get_lambda_name }}_post lambda exists:
  boto_lambda.function_present:
    - FunctionName: {{ pillar.estimated_price_get_lambda_name }}
    - Runtime: {{ pillar.lambda_runtime }}
    - Role: {{ pillar.iam_lambda_role }}
    - Handler: {{ pillar.estimated_price_get_lambda_handler }}
    - S3Bucket: {{ pillar.s3_workspace_bucket }}
    - S3Key: {{ pillar.lambda_s3_object }}
    - Description: {{ pillar.estimated_price_get_lambda_description }}
    - Timeout: {{ pillar.lambda_timeout }}
    - MemorySize: {{ pillar.lambda_memory }}
    - region: {{ pillar.aws_region }}
