
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

resource "aws_rds_cluster" "test" {
  db_subnet_group_name = aws_db_subnet_group.nondefault.name
  vpc_security_group_ids = [aws_security_group.nondefault.id]
  skip_final_snapshot = true
  master_username = "asdfasdf"
  master_password = "asdf1234!!"
}