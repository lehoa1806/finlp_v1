---

{% set envs = salt['cmd.shell']('aws dynamodb get-item --table-name notes --key \'{"key":{"S":"api_environment"}}\' --region ap-southeast-1 | python3 -c "import json, sys; print(json.load(sys.stdin)[\'Item\'][\'data\'][\'M\'])"')|load_json() %}  # noqa: 204

Ensure {{ pillar.history_get_lambda_name }} lambda exists:
  boto_lambda.function_present:
    - FunctionName: {{ pillar.history_get_lambda_name }}
    - Runtime: {{ pillar.lambda_runtime }}
    - Role: {{ pillar.iam_lambda_role }}
    - Handler: {{ pillar.history_get_lambda_handler }}
    - S3Bucket: {{ pillar.s3_workspace_bucket }}
    - S3Key: {{ pillar.lambda_s3_object }}
    - Description: {{ pillar.history_get_lambda_description }}
    - Environment:
        Variables:
          POSTGRESQL_DB: '{{ envs.dbname.S }}'
          POSTGRESQL_HOST: '{{ envs.host.S }}'
          POSTGRESQL_PASSWD: '{{ envs.password.S }}'
          POSTGRESQL_PORT: '{{ envs.port.S }}'
          POSTGRESQL_USER: '{{ envs.username.S }}'
    - Timeout: {{ pillar.lambda_timeout }}
    - MemorySize: {{ pillar.lambda_memory }}
    - region: {{ pillar.aws_region }}
