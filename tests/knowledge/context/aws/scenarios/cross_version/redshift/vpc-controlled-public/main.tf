resource "aws_vpc" "nondefault" {
  cidr_block = "10.1.1.0/24"
}

resource "aws_security_group" "nondefault" {
  vpc_id = aws_vpc.nondefault.id

  ingress {
    from_port = 5439
    protocol = "TCP"
    to_port = 5439
    cidr_blocks = ["0.0.0.0/0"]
  }
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

resource "aws_redshift_subnet_group" "nondefault" {
  name = "nondefault"
  subnet_ids = [aws_subnet.nondefault_1.id, aws_subnet.nondefault_2.id]
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.nondefault.id
}

resource "aws_route_table" "nondefault" {
  vpc_id = aws_vpc.nondefault.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "nondefault1" {
  route_table_id = aws_route_table.nondefault.id
  subnet_id = aws_subnet.nondefault_1.id
}

resource "aws_route_table_association" "nondefault2" {
  route_table_id = aws_route_table.nondefault.id
  subnet_id = aws_subnet.nondefault_2.id
}

resource "aws_redshift_cluster" "test" {
  cluster_identifier = "redshift-defaults-only"
  node_type = "dc2.large"
  master_password = "Test1234"
  master_username = "test"
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.nondefault.id]
  cluster_subnet_group_name = aws_redshift_subnet_group.nondefault.name
  publicly_accessible = true
}