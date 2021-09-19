provider "aws" {
  region = "eu-central-1"
}

resource "aws_db_instance" "test" {
  instance_class = "db.t3.micro"
  publicly_accessible = true
  allocated_storage = 50
  engine               = "mysql"
  username             = "foo"
  password             = "foobarbaz"
}