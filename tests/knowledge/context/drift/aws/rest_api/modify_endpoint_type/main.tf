resource "aws_api_gateway_rest_api" "api_gw" {
  name        = "test-rest-api"
  description = "API GW test"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_method" "method1" {
  rest_api_id   = aws_api_gateway_rest_api.api_gw.id
  resource_id   = aws_api_gateway_rest_api.api_gw.root_resource_id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "method1-int" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  resource_id = aws_api_gateway_rest_api.api_gw.root_resource_id
  http_method = aws_api_gateway_method.method1.http_method
  type        = "MOCK"
}

resource "aws_api_gateway_method" "method2" {
  rest_api_id   = aws_api_gateway_rest_api.api_gw.id
  resource_id   = aws_api_gateway_rest_api.api_gw.root_resource_id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "method2-int" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  resource_id = aws_api_gateway_rest_api.api_gw.root_resource_id
  http_method = aws_api_gateway_method.method2.http_method
  type        = "MOCK"
}

resource "aws_api_gateway_method" "method3" {
  rest_api_id   = aws_api_gateway_rest_api.api_gw.id
  resource_id   = aws_api_gateway_rest_api.api_gw.root_resource_id
  http_method   = "PUT"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "method3-int" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  resource_id = aws_api_gateway_rest_api.api_gw.root_resource_id
  http_method = aws_api_gateway_method.method3.http_method
  type        = "MOCK"
}

resource "aws_api_gateway_method" "method4" {
  rest_api_id   = aws_api_gateway_rest_api.api_gw.id
  resource_id   = aws_api_gateway_rest_api.api_gw.root_resource_id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "method4-int" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  resource_id = aws_api_gateway_rest_api.api_gw.root_resource_id
  http_method = aws_api_gateway_method.method4.http_method
  type        = "MOCK"
}
