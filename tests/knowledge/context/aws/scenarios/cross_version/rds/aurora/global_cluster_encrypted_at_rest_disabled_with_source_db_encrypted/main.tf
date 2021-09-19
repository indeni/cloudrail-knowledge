resource "aws_rds_global_cluster" "global" {
  global_cluster_identifier = "cloudrail-test-non-encrypted"
  force_destroy             = true
  source_db_cluster_identifier = "arn:aws:rds::115553109071:global-cluster:cloudrail-test-non-encrypted"
}
