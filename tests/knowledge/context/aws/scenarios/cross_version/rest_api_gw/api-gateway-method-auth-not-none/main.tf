
resource "aws_s3_bucket" "my-bucket" {
  bucket = "bucket-for-testing-api-method-auth"
}

resource "aws_s3_bucket_public_access_block" "my-bucket-access-block" {
  bucket = aws_s3_bucket.my-bucket.id
  ignore_public_acls   = true
  restrict_public_buckets = true
}

resource "aws_api_gateway_rest_api" "my-api-gateway" {
  name = "my-api-gateway"

  endpoint_configuration {
    types = ["PRIVATE"]
  }
}

resource "aws_api_gateway_resource" "my-api-gateway-resource" {
  path_part   = "v1"
  parent_id   = aws_api_gateway_rest_api.my-api-gateway.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.my-api-gateway.id
}

resource "aws_api_gateway_method" "my-api-gateway-method" {
  rest_api_id   = aws_api_gateway_rest_api.my-api-gateway.id
  resource_id   = aws_api_gateway_resource.my-api-gateway-resource.id
  http_method   = "ANY"
  authorization = "AWS_IAM"
}