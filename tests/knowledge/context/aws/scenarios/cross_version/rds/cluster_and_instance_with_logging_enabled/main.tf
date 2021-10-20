
data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_db_instance" "test" {
  allocated_storage               = 10
  engine                          = "mysql"
  engine_version                  = "5.7"
  instance_class                  = "db.t3.micro"
  name                            = "mydb"
  username                        = "foo"
  password                        = "foobarbaz"
  parameter_group_name            = "default.mysql5.7"
  skip_final_snapshot             = true
  enabled_cloudwatch_logs_exports = ["audit"]
}

resource "aws_rds_cluster" "default" {
  cluster_identifier              = "cloudrail-test-auth"
  engine                          = "aurora-mysql"
  engine_version                  = "5.7.mysql_aurora.2.03.2"
  availability_zones              = slice(data.aws_availability_zones.available.names, 0, 1)
  database_name                   = "cloudrail"
  master_username                 = "administrator"
  master_password                 = "cloudrail-TEST-password"
  skip_final_snapshot             = true
  enabled_cloudwatch_logs_exports = ["audit"]
}
