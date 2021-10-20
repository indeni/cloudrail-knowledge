resource "aws_vpc" "nondefault" {
  cidr_block = "10.1.1.0/24"
}

resource "aws_security_group" "nondefault" {
  vpc_id = aws_vpc.nondefault.id
}

resource "aws_subnet" "nondefault_1" {
  vpc_id = aws_vpc.nondefault.id
  cidr_block = "10.1.1.128/25"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "nondefault_2" {
  vpc_id = aws_vpc.nondefault.id
  cidr_block = "10.1.1.0/25"
  availability_zone = "us-east-1b"
}

resource "aws_db_subnet_group" nondefault {
  name = "nondefault"
  subnet_ids = [
    aws_subnet.nondefault_1.id,
    aws_subnet.nondefault_2.id]
}

resource "aws_db_instance" "test" {
  instance_class = "db.t3.micro"
  publicly_accessible = false
  db_subnet_group_name = aws_db_subnet_group.nondefault.name
  vpc_security_group_ids = [aws_security_group.nondefault.id]
  allocated_storage = 20
  storage_type = "gp2"
  engine = "mysql"
  engine_version = "5.7"
  name = "mydb"
  username = "foo"
  password = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot = true
}