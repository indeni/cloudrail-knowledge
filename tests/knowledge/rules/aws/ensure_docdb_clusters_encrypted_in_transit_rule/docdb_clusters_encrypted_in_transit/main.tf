provider "aws" {
  region = "us-east-1"
}

resource "aws_docdb_cluster" "test" {
  cluster_identifier  = "in-transit-encryp-enabled"
  engine              = "docdb"
  master_username     = "foo"
  master_password     = "mustbeeightchars"
  skip_final_snapshot = true
}
