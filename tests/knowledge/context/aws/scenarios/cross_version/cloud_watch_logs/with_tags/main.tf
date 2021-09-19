

resource "aws_cloudwatch_log_group" "cloudrail-test" {
  retention_in_days = 1
  tags = {
    Environment = "production"
    Application = "serviceA"
  }
}
