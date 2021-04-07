---
include:
  - common

api_gateway_name: warrant
api_gateway_description: A RESTful API Gateway endpoint for Warrant Dashboard
api_gateway_resources:
  info:
    - get

usage_plan_name: web_warrant_basic

# Lambda name is always in {api}_{resource}_{method} format if we want to use it in an Api Gateway
warrant_info_get_lambda_name: warrant_info_get
warrant_info_get_lambda_handler: lambdas.warrant_info.lambda_handlers.warrant_info_get.lambda_handler
warrant_info_get_lambda_description: Get data for Warrant Dashboard
