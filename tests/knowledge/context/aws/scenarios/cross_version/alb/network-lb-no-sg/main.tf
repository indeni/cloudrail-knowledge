resource "aws_vpc" "external" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "external" {
  cidr_block = "10.0.0.0/24"
  vpc_id = aws_vpc.external.id
}

resource "aws_lb" "main" {
  name               = "my-lb"
  internal           = false
  load_balancer_type = "network"
  subnets            = [aws_subnet.external.id]
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.external.id
}

