resource "aws_db_instance" "test" {
  allocated_storage = 20
  storage_type = "gp2"
  engine = "mysql"
  engine_version = "5.7"
  instance_class = "db.t2.micro"
  name = "mydb"
  username = "foo"
  password = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot = true
}