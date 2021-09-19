provider "aws" {
  region = "us-east-1"
}

resource "aws_docdb_cluster" "test" {
  cluster_identifier              = "in-transit-encryp-disabled"
  engine                          = "docdb"
  master_username                 = "foo"
  master_password                 = "mustbeeightchars"
  skip_final_snapshot             = true
  db_cluster_parameter_group_name = aws_docdb_cluster_parameter_group.test.id
}

resource "aws_docdb_cluster_parameter_group" "test" {
  family      = "docdb3.6"
  name        = "in-transit-encryp-disabled"
  description = "in-transit-encryp-disabled"

  parameter {
    name  = "tls"
    value = "disabled"
  }
}
