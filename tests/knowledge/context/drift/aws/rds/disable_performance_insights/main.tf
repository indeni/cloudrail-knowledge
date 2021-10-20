resource "aws_vpc" "nondefault" {
  cidr_block = "10.1.1.0/24"
}

resource "aws_security_group" "nondefault" {
  vpc_id = aws_vpc.nondefault.id
}

resource "aws_subnet" "nondefault_1" {
  vpc_id            = aws_vpc.nondefault.id
  cidr_block        = "10.1.1.128/25"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "nondefault_2" {
  vpc_id            = aws_vpc.nondefault.id
  cidr_block        = "10.1.1.0/25"
  availability_zone = "us-east-1b"
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.nondefault.id

  tags = {
    Name = "main"
  }
}

resource "aws_default_route_table" "ido_default_route_table" {
  default_route_table_id = aws_vpc.nondefault.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
  tags = {
    Name = "default table"
  }
}

resource "aws_db_subnet_group" "nondefault" {
  name = "nondefault"
  subnet_ids = [
    aws_subnet.nondefault_1.id,
  aws_subnet.nondefault_2.id]
}

resource "aws_db_instance" "test" {
  allocated_storage            = 20
  storage_type                 = "gp2"
  engine                       = "postgres"
  engine_version               = "11.10"
  instance_class               = "db.t2.micro"
  name                         = "mydb"
  username                     = "foo"
  password                     = "foobarbaz"
  skip_final_snapshot          = true
  performance_insights_enabled = true
  db_subnet_group_name         = aws_db_subnet_group.nondefault.name
  vpc_security_group_ids       = [aws_security_group.nondefault.id]
}