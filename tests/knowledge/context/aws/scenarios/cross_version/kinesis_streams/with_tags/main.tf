
resource "aws_kinesis_stream" "cloudrail" {
  name        = "cloudrail-test-non-encrypted"
  shard_count = 1
  tags = {
    Name = "Cloudrail Kinesis test"
  }
}
