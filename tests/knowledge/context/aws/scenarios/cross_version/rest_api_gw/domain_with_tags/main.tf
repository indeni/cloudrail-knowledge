
locals {
  zone_id     = aws_route53_zone.current.zone_id
  api_gw_name = "api.${aws_route53_zone.current.name}"
}

resource "aws_route53_zone" "current" {
  name = "cloudrail-testing.com"
}

resource "aws_route53_record" "example" {
  allow_overwrite = true
  name            = tolist(aws_acm_certificate.example.domain_validation_options)[0].resource_record_name
  records         = [tolist(aws_acm_certificate.example.domain_validation_options)[0].resource_record_value]
  ttl             = 60
  type            = tolist(aws_acm_certificate.example.domain_validation_options)[0].resource_record_type
  zone_id         = local.zone_id
}

resource "aws_acm_certificate" "example" {
  domain_name       = local.api_gw_name
  validation_method = "DNS"
}

resource "aws_acm_certificate_validation" "example" {
  certificate_arn         = aws_acm_certificate.example.arn
  validation_record_fqdns = [aws_route53_record.example.fqdn]
}

resource "aws_api_gateway_base_path_mapping" "test" {
  api_id      = aws_api_gateway_rest_api.api_gw.id
  stage_name  = aws_api_gateway_deployment.api_gw_deploy.stage_name
  domain_name = aws_api_gateway_domain_name.example.domain_name
}

resource "aws_api_gateway_rest_api" "api_gw" {
  name        = "api-gw-cache-encrypted"
  description = "API GW test"
}

resource "aws_api_gateway_deployment" "api_gw_deploy" {
  depends_on  = [aws_api_gateway_integration.api_gw_int]
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  stage_name  = "dev"
}

resource "aws_api_gateway_resource" "api_gw_resource" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  parent_id   = aws_api_gateway_rest_api.api_gw.root_resource_id
  path_part   = "mytestresource"
}

resource "aws_api_gateway_method" "api_gw_method" {
  rest_api_id   = aws_api_gateway_rest_api.api_gw.id
  resource_id   = aws_api_gateway_resource.api_gw_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "api_gw_int" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  resource_id = aws_api_gateway_resource.api_gw_resource.id
  http_method = aws_api_gateway_method.api_gw_method.http_method
  type        = "MOCK"

  request_templates = {
    "application/xml" = <<EOF
{
   "body" : $input.json('$')
}
EOF
  }
}

resource "aws_api_gateway_stage" "api_gw_stage" {
  stage_name    = "prod"
  rest_api_id   = aws_api_gateway_rest_api.api_gw.id
  deployment_id = aws_api_gateway_deployment.api_gw_deploy.id
}

resource "aws_api_gateway_method_settings" "api_gw_method_sett" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  stage_name  = aws_api_gateway_stage.api_gw_stage.stage_name
  method_path = "${aws_api_gateway_resource.api_gw_resource.path_part}/${aws_api_gateway_method.api_gw_method.http_method}"

  settings {
    logging_level        = "OFF"
    caching_enabled      = true # This is required for cache encryption
    cache_data_encrypted = true # This is required for cache encryption
  }
}
resource "aws_api_gateway_domain_name" "example" {
  domain_name              = local.api_gw_name
  regional_certificate_arn = aws_acm_certificate_validation.example.certificate_arn
  tags = {
    Name = "Api test"
  }
  security_policy = "TLS_1_2"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}
