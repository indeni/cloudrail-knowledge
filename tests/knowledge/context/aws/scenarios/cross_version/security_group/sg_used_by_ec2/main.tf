resource "aws_vpc" "VPC" {
  cidr_block = "10.1.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "my-vpc"
  }
}

resource "aws_subnet" "PublicSubnet1" {
  cidr_block = "10.1.0.0/24"
  map_public_ip_on_launch = true
  vpc_id = aws_vpc.VPC.id

  tags = {
    Name = "Public Subnet AZ A"
  }
}

resource "aws_security_group" "inbound_to_lb" {
  description = "A distinct description"
  name = "distinct_name"
  vpc_id = aws_vpc.VPC.id
  ingress {
    from_port = 80
    protocol = "TCP"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "linux" {
  ami           = "ami-032930428bf1abbff"
  instance_type = "t2.micro"
  security_groups = [aws_security_group.inbound_to_lb.id]
  subnet_id = aws_subnet.PublicSubnet1.id
  associate_public_ip_address = "false"

  tags = {
    Name = "Linux Instance"
  }
}