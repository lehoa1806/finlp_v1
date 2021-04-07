---
include:
  - common

api_gateway_name: warrant
api_gateway_description: A RESTful API Gateway endpoint for Warrant Dashboard
api_gateway_resources:
  info:
    - get
  estimatedPrice:
    - get
    - post

usage_plan_name: web_warrant_basic

# Lambda name is always in {api}_{resource}_{method} format if we want to use it in an Api Gateway
warrant_info_get_lambda_name: warrant_info_get
warrant_info_get_lambda_handler: lambdas.warrant_info.lambda_handlers.warrant_info_get.lambda_handler
warrant_info_get_lambda_description: Get data for Warrant Dashboard

estimated_price_get_lambda_name: warrant_estimatedprice_get
estimated_price_get_lambda_handler: lambdas.warrant_info.lambda_handlers.estimated_price_get.lambda_handler
estimated_price_get_lambda_description: Get estimated prices for Warrant Dashboard

estimated_price_post_lambda_name: warrant_estimatedprice_post
estimated_price_post_lambda_handler: lambdas.warrant_info.lambda_handlers.estimated_price_post.lambda_handler
estimated_price_post_lambda_description: Update estimated prices from Warrant Dashboard
