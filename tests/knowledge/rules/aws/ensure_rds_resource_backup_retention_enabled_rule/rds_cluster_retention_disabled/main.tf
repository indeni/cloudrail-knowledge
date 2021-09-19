provider "aws" {
  region = "us-east-1"
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_rds_cluster" "test" {
  cluster_identifier      = "rds-test-backup"
  engine                  = "aurora-mysql"
  engine_version          = "5.7.mysql_aurora.2.03.2"
  availability_zones      = data.aws_availability_zones.available.names
  database_name           = "cloudrail"
  master_username         = "administrator"
  master_password         = "cloudrail-TEST-password"
  skip_final_snapshot     = true
  backup_retention_period = 0
}
