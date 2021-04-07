---
include:
  - iam_api_gateway_role

{% set now = None | strftime("%Y-%m-%dT%H:%M:%SZ") %}
{% set swagger_file = '/tmp/workspace/swagger.yml' %}

create a temporary workspace for {{ swagger_file }}:
  cmd.run:
    - names:
        - rm -rf /tmp/workspace
        - mkdir -p /tmp/workspace
        - touch /tmp/workspace/swagger.yml
    - runas: {{ pillar.user_name }}

initialize the swagger template:
  file.append:
    - name: {{ swagger_file }}
    - text: |2
        ---
        swagger: "2.0"
        info:
          description: "{{ pillar.api_gateway_description }}"
          version: "{{ now }}"
          title: "{{ pillar.api_gateway_name }}"
        basePath: "/{{ pillar.api_gateway_name }}"
        schemes:
        - "https"
        paths:

{% for resource_name, methods in pillar.get('api_gateway_resources', {}).items() %}
append {{ resource_name }} to swagger file:
  file.append:
    - name: {{ swagger_file }}
    - text: |2
          /{{ resource_name }}:

{% for method in methods %}
create a temporary file for {{ swagger_file }}_{{ method }}_{{ resource_name }}:
  cmd.run:
    - name: touch {{ swagger_file }}_{{ method }}_{{ resource_name }}
    - runas: {{ pillar.user_name }}

append {{ method }} to {{ resource_name }} temporary file:
  file.append:
    - name: {{ swagger_file }}_{{ method }}_{{ resource_name }}
    - text: |2
            {{ method }}:
              consumes:
              - "application/json"
              produces:
              - "application/json"
              responses:
                200:
                  description: "200 response"
                  schema:
                    $ref: "#/definitions/Empty"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
                400:
                  description: "400 response"
                  schema:
                    $ref: "#/definitions/BadRequest"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
                401:
                  description: "401 response"
                  schema:
                    $ref: "#/definitions/Unauthorized"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
                403:
                  description: "403 response"
                  schema:
                    $ref: "#/definitions/Forbidden"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
                500:
                  description: "500 response"
                  schema:
                    $ref: "#/definitions/InternalServerError"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
              security:
              - sigv4: []
              x-amazon-apigateway-integration:
                credentials: "{{ pillar.iam_api_gateway_role }}"
                uri: "arn:aws:apigateway:{{ pillar.aws_region }}:lambda:path/2015-03-31/functions/arn:aws:lambda:{{ pillar.aws_region }}:{{ pillar.aws_account_id }}:function:{{ pillar.api_gateway_name }}_{{ resource_name }}_{{ method }}/invocations"
                passthroughBehavior: "when_no_match"
                type: "aws"
                responses:
                  default:
                    statusCode: "200"
                  .*Bad Request.*:
                    statusCode: "400"
                  .*Unauthorized.*:
                    statusCode: "401"
                  .*Forbidden.*:
                    statusCode: "403"
                  .*Internal Server Error.*:
                    statusCode: "500"

append {{ method }}_{{ resource_name }} temporary file to swagger file:
  cmd.run:
    - name: cat {{ swagger_file }}_{{ method }}_{{ resource_name }} >> {{ swagger_file }}
    - runas: {{ pillar.user_name }}
{% endfor %}

append option to {{ resource_name }}:
  file.append:
    - name: {{ swagger_file }}
    - text: |2
            option:
              consumes:
              - "application/json"
              produces:
              - "application/json"
              responses:
                200:
                  description: "200 response"
                  schema:
                    $ref: "#/definitions/Empty"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
                    Access-Control-Allow-Methods:
                      type: "string"
                    Access-Control-Allow-Headers:
                      type: "string"
                400:
                  description: "400 response"
                  schema:
                    $ref: "#/definitions/BadRequest"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
                    Access-Control-Allow-Methods:
                      type: "string"
                    Access-Control-Allow-Headers:
                      type: "string"
                401:
                  description: "401 response"
                  schema:
                    $ref: "#/definitions/Unauthorized"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
                    Access-Control-Allow-Methods:
                      type: "string"
                    Access-Control-Allow-Headers:
                      type: "string"
                403:
                  description: "403 response"
                  schema:
                    $ref: "#/definitions/Forbidden"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
                    Access-Control-Allow-Methods:
                      type: "string"
                    Access-Control-Allow-Headers:
                      type: "string"
                500:
                  description: "500 response"
                  schema:
                    $ref: "#/definitions/InternalServerError"
                  headers:
                    Access-Control-Allow-Origin:
                      type: "string"
                    Access-Control-Allow-Methods:
                      type: "string"
                    Access-Control-Allow-Headers:
                      type: "string"
              x-amazon-apigateway-integration:
                responses:
                  .*:
                    statusCode: "200"
                    responseParameters:
                      method.response.header.Access-Control-Allow-Methods: "'*'"
                      method.response.header.Access-Control-Allow-Headers: "'*'"
                      method.response.header.Access-Control-Allow-Origin: "'*'"
                requestTemplates:
                  application/json: "{\"statusCode\": 200}"
                passthroughBehavior: "when_no_match"
                type: "mock"
{% endfor %}

append definitions to {{ swagger_file }}:
  file.append:
    - name: {{ swagger_file }}
    - text: |2
        definitions:
          Empty:
            type: "object"
            properties:
              message:
                type: "string"
            title: "Empty Schema"
            pattern: "-"
          BadRequest:
            type: "object"
            properties:
              status:
                type: "integer"
                format: "int32"
              errorMessage:
                type: "string"
            title: "Bad Request Schema"
            pattern: ".*Bad Request.*"
          InternalServerError:
            type: "object"
            properties:
              status:
                type: "integer"
                format: "int32"
              errorMessage:
                type: "string"
            title: "Internal Server Error Schema"
            pattern: ".*Internal Server Error.*"
          Unauthorized:
            type: "object"
            properties:
              status:
                type: "integer"
                format: "int32"
              errorMessage:
                type: "string"
            title: "Unauthorized Schema"
            pattern: ".*Unauthorized.*"
          Forbidden:
            type: "object"
            properties:
              status:
                type: "integer"
                format: "int32"
              errorMessage:
                type: "string"
            title: "Forbidden Schema"
            pattern: ".*Forbidden.*"

create {{ pillar.api_gateway_name }}:
  boto_apigateway.present:
    - api_name: {{ pillar.api_gateway_name }}
    - swagger_file: {{ swagger_file }}
    - stage_name: {{ pillar.api_gateway_stage }}
    - region: {{ pillar.aws_region }}
    - api_key_required: {{ pillar.api_key_required }}
    - lambda_integration_role: {{ pillar.iam_api_gateway_role }}
    - lambda_region: {{ pillar.aws_region }}
    - lambda_funcname_format: {{ pillar.lambda_name_format }}
    - authorization_type: {{ pillar.authorization_type }}
    - response_template: {{ pillar.response_template }}
    - error_response_template: {{ pillar.error_response_template }}
