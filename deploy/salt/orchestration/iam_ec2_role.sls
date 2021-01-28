---
create {{ pillar.iam_ec2_role }} IAM role:
  boto_iam_role.present:
    - name: {{ pillar.iam_ec2_role }}
    - region: {{ pillar.aws_region }}
    - policy_document:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal: {
              Service: 'ec2.amazonaws.com'
            }
        Version: '{{ pillar.iam_version }}'
    - policies:
        DeveloperEc2IamRole:
          Statement:
            - Action:
                - apigateway:*
                - dynamodb:*
                - ec2:*
                - iam:*
                - lambda:*
                - logs:*
                - s3:*
              Effect: Allow
              Resource: '*'
          Version: '{{ pillar.iam_version }}'
