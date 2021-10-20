

resource "aws_kms_key" "testing-tags" {
  description             = "KMS key for testing cloudrail tags"
  deletion_window_in_days = 7
  tags = {
    Name = "testing-tags",
    Env = "Cloudrail Rocks"
  }
}