
resource "aws_dynamodb_table" "basic-dynamodb-table-1" {
  name           = "GameScores"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 10
  hash_key       = "UserId"
  range_key      = "GameTitle"

  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "GameTitle"
    type = "S"
  }
  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}
