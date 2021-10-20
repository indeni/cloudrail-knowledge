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

resource "aws_redshift_subnet_group" nondefault {
  name = "nondefault"
  subnet_ids = [aws_subnet.nondefault_1.id, aws_subnet.nondefault_2.id]

}
resource "aws_redshift_cluster" "test" {
  cluster_identifier = "redshift-defaults-only"
  node_type = "dc2.large"
  master_password = "Test1234"
  master_username = "test"
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.nondefault.id]
  cluster_subnet_group_name = aws_redshift_subnet_group.nondefault.name
  publicly_accessible = false
}