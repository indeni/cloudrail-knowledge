provider "aws" {
  region = "us-east-1"
}

resource "aws_kinesis_stream" "cloudrail" {
  name            = "cloudrail-test-encrypted"
  shard_count     = 1
  encryption_type = "KMS"
  kms_key_id      = "alias/aws/kinesis"
}

resource "aws_kinesis_stream" "cloudrail_2" {
  name            = "cloudrail-test-encrypted_2"
  shard_count     = 1
  encryption_type = "KMS"
  kms_key_id      = "alias/aws/kinesis"
}
