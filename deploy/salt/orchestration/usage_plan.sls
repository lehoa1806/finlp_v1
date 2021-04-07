---
Ensure Usage plan of {{ pillar.api_name }} exists:
  boto_apigateway.usage_plan_present:
    - plan_name: {{ pillar.usage_plan_name }}
    - throttle:
        rateLimit: 70
        burstLimit: 100
    - quota:
        limit: 1000
        offset: 0
        period: DAY
