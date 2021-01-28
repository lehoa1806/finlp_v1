---
create {{ pillar.iam_lambda_role }}:
  boto_iam_role.present:
    - name: {{ pillar.iam_lambda_role }}
    - region: {{ pillar.aws_region }}
    - policy_document:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal: {
              Service: [
                lambda.amazonaws.com
              ]
            }
        Version: '{{ pillar.iam_version }}'
    - policies:
        UserLambdaIamRole:
          Statement:
            - Action:
                - dynamodb:*
                - lambda:*
                - logs:*
                - s3:*
                - sqs:*
              Effect: Allow
              Resource: '*'
          Version: '{{ pillar.iam_version }}'
