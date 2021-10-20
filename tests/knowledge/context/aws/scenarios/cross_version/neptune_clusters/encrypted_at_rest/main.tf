resource "aws_neptune_cluster" "test" {
  cluster_identifier  = "cloudrail-test-encrypted"
  engine              = "neptune"
  skip_final_snapshot = true
  apply_immediately   = true
  storage_encrypted   = true
}
