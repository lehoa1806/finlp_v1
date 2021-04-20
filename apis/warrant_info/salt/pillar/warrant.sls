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
  dashboard:
    - get
  userInfo:
    - get
    - post
  history:
    - get
    - post

usage_plan_name: web_warrant_basic

# Lambda name is always in {api}_{resource}_{method} format if we want to use it in an Api Gateway
warrant_info_get_lambda_name: warrant_info_get
warrant_info_get_lambda_handler: apis.warrant_info.lambda_handlers.warrant_info_get.lambda_handler
warrant_info_get_lambda_description: Get data for Warrant Dashboard

warrant_dashboard_get_lambda_name: warrant_dashboard_get
warrant_dashboard_get_lambda_handler: apis.warrant_info.lambda_handlers.warrant_dashboard_get.lambda_handler
warrant_dashboard_get_lambda_description: Get initial data for Warrant Dashboard

estimated_price_get_lambda_name: warrant_estimatedprice_get
estimated_price_get_lambda_handler: apis.warrant_info.lambda_handlers.estimated_price_get.lambda_handler
estimated_price_get_lambda_description: Get estimated prices for Warrant Dashboard

estimated_price_post_lambda_name: warrant_estimatedprice_post
estimated_price_post_lambda_handler: apis.warrant_info.lambda_handlers.estimated_price_post.lambda_handler
estimated_price_post_lambda_description: Update estimated prices from Warrant Dashboard

user_info_get_lambda_name: warrant_userinfo_get
user_info_get_lambda_handler: apis.warrant_info.lambda_handlers.user_info_get.lambda_handler
user_info_get_lambda_description: Get watchlist, portfolio for Warrant Dashboard

user_info_post_lambda_name: warrant_userinfo_post
user_info_post_lambda_handler: apis.warrant_info.lambda_handlers.user_info_post.lambda_handler
user_info_post_lambda_description: Update watchlist, portfolio from Warrant Dashboard

history_get_lambda_name: warrant_history_get
history_get_lambda_handler: apis.warrant_info.lambda_handlers.history_get.lambda_handler
history_get_lambda_description: Get trading records for Warrant Dashboard

history_post_lambda_name: warrant_history_post
history_post_lambda_handler: apis.warrant_info.lambda_handlers.history_post.lambda_handler
history_post_lambda_description: Update trading records from Warrant Dashboard
