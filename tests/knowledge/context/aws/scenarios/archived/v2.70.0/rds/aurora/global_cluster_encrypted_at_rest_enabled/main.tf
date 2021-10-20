resource "aws_rds_global_cluster" "global" {
  global_cluster_identifier = "cloudrail-test-encrypted"
  storage_encrypted         = true
}
