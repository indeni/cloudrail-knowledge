provider "aws" {
  region = "us-east-1"
}

resource "aws_redshift_cluster" "test" {
  cluster_identifier  = "cloudrail-redshift-cluster-logging"
  database_name       = "mydb"
  master_username     = "administrator"
  master_password     = "Zasdf8adf887"
  node_type           = "dc1.large"
  cluster_type        = "single-node"
  skip_final_snapshot = true
}
