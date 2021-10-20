resource "aws_db_subnet_group" "prod" {
  subnet_ids = module.serverlessProduction.private_subnets
}

resource "aws_db_instance" "prod" {
  count                = local.projects["serverlessProduction"].num_rds_instances
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = "foo"
  password             = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
  db_subnet_group_name = aws_db_subnet_group.prod.id
}

resource "aws_db_subnet_group" "stag" {
  subnet_ids = module.serverlessStaging.private_subnets
}

resource "aws_db_instance" "stag" {
  count                = local.projects["serverlessStaging"].num_rds_instances
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = "foo"
  password             = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
  db_subnet_group_name = aws_db_subnet_group.stag.id
}

resource "aws_db_subnet_group" "test" {
  subnet_ids = module.serverlessTesting.private_subnets
}

resource "aws_db_instance" "test" {
  count                = local.projects["serverlessTesting"].num_rds_instances
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = "foo"
  password             = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
  db_subnet_group_name = aws_db_subnet_group.test.id
}
