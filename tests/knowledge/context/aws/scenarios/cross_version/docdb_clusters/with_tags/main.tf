
resource "aws_docdb_cluster" "test" {
  cluster_identifier              = "in-transit-encryp-disabled"
  engine                          = "docdb"
  master_username                 = "foo"
  master_password                 = "mustbeeightchars"
  skip_final_snapshot             = true
  db_cluster_parameter_group_name = aws_docdb_cluster_parameter_group.test.id
  tags = {
    Name = "DocDB cluster Cloudrail"
  }
}

resource "aws_docdb_cluster_parameter_group" "test" {
  family      = "docdb4.0"
  name        = "in-transit-encryp-disabled"
  description = "in-transit-encryp-disabled"
  tags = {
    Name = "Docdb Param Group Cloudrail"
  }

  parameter {
    name  = "tls"
    value = "disabled"
  }
}
