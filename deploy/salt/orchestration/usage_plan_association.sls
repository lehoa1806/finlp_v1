---
include:
  - common

{% set api_id = salt['boto_apigateway.describe_apis'](name=pillar.api_gateway_name, region=pillar.aws_region).get('restapi')[0].get('id') %}

Ensure usage plan identified by {{ pillar.usage_plan_name }} is added to {{ pillar.api_gateway_name }}:
  boto_apigateway.usage_plan_association_present:
    - plan_name: {{ pillar.usage_plan_name }}
    - api_stages:
      - apiId: {{ api_id }}
        stage: {{ pillar.api_gateway_stage }}
    - region: {{ pillar.aws_region }}
