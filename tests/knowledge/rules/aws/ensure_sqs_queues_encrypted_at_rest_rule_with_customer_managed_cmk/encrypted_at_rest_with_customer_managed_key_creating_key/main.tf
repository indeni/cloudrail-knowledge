provider "aws" {
  region = "us-east-1"
}

resource "aws_kms_key" "test" {
  description             = "customer-managed CMK for SQS test"
  deletion_window_in_days = 7
}

resource "aws_sqs_queue" "test" {
  name              = "sqs_encrypted"
  kms_master_key_id = aws_kms_key.test.arn
}
