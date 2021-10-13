provider "aws" {
  region = "us-east-1"
}

data "aws_kms_key" "by_alias" {
  key_id = "alias/test-sqs"
}

resource "aws_sqs_queue" "test" {
  name              = "sqs_encrypted"
  kms_master_key_id = data.aws_kms_key.by_alias.arn
}
