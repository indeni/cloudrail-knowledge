
resource "aws_kms_key" "test" {
  description             = "KMS key for DynamoDB"
  deletion_window_in_days = 7
}

resource "aws_dynamodb_table" "test" {
  name           = "cloudrail-test"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.test.arn
  }
}
