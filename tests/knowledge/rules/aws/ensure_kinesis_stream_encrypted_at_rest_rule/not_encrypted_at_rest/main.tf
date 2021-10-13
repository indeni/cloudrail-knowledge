provider "aws" {
  region = "us-east-1"
}

resource "aws_kinesis_stream" "cloudrail" {
  name        = "cloudrail-test-non-encrypted"
  shard_count = 1
}

resource "aws_kinesis_stream" "cloudrail_2" {
  name        = "cloudrail-test-non-encrypted_2"
  shard_count = 1
}
