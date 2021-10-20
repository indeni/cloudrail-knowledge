
data "aws_kms_key" "by_alias" {
  key_id = "alias/aws/dynamodb"
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
    kms_key_arn = data.aws_kms_key.by_alias.arn
  }
}
