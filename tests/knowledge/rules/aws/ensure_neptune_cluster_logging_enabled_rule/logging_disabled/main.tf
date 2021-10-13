provider "aws" {
  region = "us-east-1"
}

resource "aws_neptune_cluster" "test" {
  cluster_identifier  = "test-no-logging"
  engine              = "neptune"
  skip_final_snapshot = true
  apply_immediately   = true
}
