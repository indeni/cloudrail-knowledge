
resource "aws_docdb_cluster" "test" {
  cluster_identifier              = "docdb-no-logging"
  engine                          = "docdb"
  master_username                 = "foo"
  master_password                 = "mustbeeightchars"
  skip_final_snapshot             = true
  enabled_cloudwatch_logs_exports = ["audit", "profiler"]
}
