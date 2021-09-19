
resource "aws_neptune_cluster" "test" {
  cluster_identifier             = "test-logging"
  engine                         = "neptune"
  skip_final_snapshot            = true
  apply_immediately              = true
  enable_cloudwatch_logs_exports = ["audit"]
}
