resource "aws_kms_key" "test" {
  description             = "KMS key for RDS"
  deletion_window_in_days = 7
}

resource "aws_neptune_cluster" "test" {
  cluster_identifier  = "cloudrail-test-encrypted"
  engine              = "neptune"
  skip_final_snapshot = true
  apply_immediately   = true
  storage_encrypted   = true
  kms_key_arn         = aws_kms_key.test.arn
}
