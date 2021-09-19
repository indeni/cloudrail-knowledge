provider "aws" {
  region = "us-east-1"
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_db_instance" "test" {
  allocated_storage   = 10
  engine              = "mariadb"
  engine_version      = "10.5.8"
  instance_class      = "db.t3.micro"
  name                = "mydb"
  username            = "foo"
  password            = "foobarbaz"
  skip_final_snapshot = true
}
