---
Ensure {{ pillar.history_post_lambda_name }} lambda exists:
  boto_lambda.function_present:
    - FunctionName: {{ pillar.history_post_lambda_name }}
    - Runtime: {{ pillar.lambda_runtime }}
    - Role: {{ pillar.iam_lambda_role }}
    - Handler: {{ pillar.history_post_lambda_handler }}
    - S3Bucket: {{ pillar.s3_workspace_bucket }}
    - S3Key: {{ pillar.lambda_s3_object }}
    - Description: {{ pillar.history_post_lambda_description }}
    - Timeout: {{ pillar.lambda_timeout }}
    - MemorySize: {{ pillar.lambda_memory }}
    - region: {{ pillar.aws_region }}
