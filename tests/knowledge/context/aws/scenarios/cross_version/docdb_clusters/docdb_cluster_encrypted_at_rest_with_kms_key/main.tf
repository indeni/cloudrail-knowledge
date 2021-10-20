
resource "aws_kms_key" "test" {
  description             = "KMS key for DocDB"
  deletion_window_in_days = 7
}

resource "aws_docdb_cluster" "test0" {
  cluster_identifier  = "my-docdb-cluster-test0"
  engine              = "docdb"
  master_username     = "foo"
  master_password     = "mustbeeightchars"
  skip_final_snapshot = true
  storage_encrypted   = true
  kms_key_id          = aws_kms_key.test.arn
}
