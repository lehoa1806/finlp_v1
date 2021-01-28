---
create {{ pillar.iam_api_gateway_role }}:
  boto_iam_role.present:
    - name: {{ pillar.iam_api_gateway_role }}
    - region: {{ pillar.aws_region }}
    - policy_document:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal: {
              Service: [
                apigateway.amazonaws.com,
                lambda.amazonaws.com
              ]
            }
        Version: '{{ pillar.iam_version }}'
    - policies:
        UserApiGatewayIamRole:
          Statement:
            - Action:
                - apigateway:*
                - dynamodb:*
                - lambda:*
                - logs:*
                - s3:*
                - sqs:*
              Effect: Allow
              Resource: '*'
          Version: '{{ pillar.iam_version }}'
