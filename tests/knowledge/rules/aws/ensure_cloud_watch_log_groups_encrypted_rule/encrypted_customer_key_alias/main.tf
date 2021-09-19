provider "aws" {
  region = "us-east-1"
}

data "aws_kms_key" "by_alias" {
  key_id = "alias/test-log-group"
}

resource "aws_cloudwatch_log_group" "cloudrail-test" {
  retention_in_days = 1
  kms_key_id        = data.aws_kms_key.by_alias.arn
}
