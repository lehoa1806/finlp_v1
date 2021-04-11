---
include:
  - common

api_gateway_name: example
api_gateway_description: A RESTful API Gateway endpoint
api_gateway_resources:
  restful:
    - get
    - post

# Lambda name is always in {api}_{resource}_{method} format if we want to use it in an Api Gateway
example_restful_get_lambda_name: example_restful_get
example_restful_get_lambda_handler: apis.example.lambda_handlers.example_restful_get.lambda_handler
example_restful_get_lambda_description: Show search keys of the given Subscriber

example_restful_post_lambda_name: example_restful_post
example_restful_post_lambda_handler: apis.example.lambda_handlers.example_restful_post.lambda_handler
example_restful_post_lambda_description: Show search keys of the given Subscriber
