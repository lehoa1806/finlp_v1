---

{% set secret_bucket = 'finulp-secrets' %}
{% set news_bucket = 'finulp-news' %}

create {{ pillar.iam_ec2_role }} IAM role:
  boto_iam_role.present:
    - name: {{ pillar.iam_role }}
    - region: {{ pillar.aws_region }}
    - policy_document:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal: {
              Service: 'ec2.amazonaws.com'
            }
        Version: '2012-10-17'
    - policies:
        DeveloperEc2IamRole:
          Statement:
            - Action:
                - dynamodb:*
                - ec2:*
                - s3:*
              Effect: Allow
              Resource:
                - 'arn:aws:s3:::{{ secret_bucket }/*'
                - 'arn:aws:s3:::{{ news_bucket }/*'
                - 'arn:aws:dynamodb:::*'
          Version: '2012-10-17'
