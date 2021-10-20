resource "aws_rds_cluster" "default" {
  cluster_identifier  = "cloudrail-test-encrypted"
  engine              = "aurora-mysql"
  engine_version      = "5.7.mysql_aurora.2.03.2"
  availability_zones  = ["us-east-1a", "us-east-1b", "us-east-1c"]
  database_name       = "cloudrail"
  master_username     = "administrator"
  master_password     = "cloudrail-TEST-password"
  skip_final_snapshot = true
  storage_encrypted   = true
}
