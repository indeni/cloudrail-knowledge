data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "vpc1" {
  cidr_block = "10.10.0.0/16"
}

resource "aws_subnet" "subnet1" {
  vpc_id = aws_vpc.vpc1.id
  cidr_block = "10.10.10.0/24"
  availability_zone_id = data.aws_availability_zones.available.zone_ids[0]
  tags = {
    Name = "subnet1"
  }
}

resource "aws_subnet" "subnet2" {
  vpc_id = aws_vpc.vpc1.id
  cidr_block = "10.10.11.0/24"
  availability_zone_id = data.aws_availability_zones.available.zone_ids[1]

  tags = {
    Name = "subnet2"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc1.id
}

resource "aws_eip" "example1" {
  vpc = true
}

resource "aws_eip" "example2" {
  vpc = true
}

resource "aws_lb" "test" {
  name = "test123"
  load_balancer_type = "network"
  internal = false
  subnet_mapping {
    subnet_id = aws_subnet.subnet1.id
    allocation_id = aws_eip.example1.id
  }
  subnet_mapping {
    subnet_id = aws_subnet.subnet2.id
    allocation_id = aws_eip.example2.id
  }
}