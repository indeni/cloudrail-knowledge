provider "aws" {
  region = "us-east-1"
}

resource "aws_autoscaling_group" "test-autoscaling-group" {
  name                      = "test-autoscaling-group"
  max_size                  = 5
  min_size                  = 2

  launch_template {
    id      = aws_launch_template.test-launch-template.id
    version = "$Latest"
  }
}

resource "aws_launch_template" "test-launch-template" {
  name = "test-launch-template"
  image_id      = "ami-1a2b3c"
  instance_type = "t2.micro"

  network_interfaces {
    associate_public_ip_address = true
    security_groups = [aws_security_group.allow-ssh.id]
    subnet_id = aws_subnet.public-subnet.id
  }

}

resource "aws_vpc" "main" {
  cidr_block = "172.16.0.0/16"
}

resource "aws_subnet" "public-subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "172.16.100.0/24"
  map_public_ip_on_launch = false
  availability_zone = "us-east-1a"

  tags = {
    Name = "public-subnet"
  }
}

resource "aws_security_group" "allow-ssh" {
  description = "allow ssh"
  ingress {
    from_port = 22
    protocol = "TCP"
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public-route-table" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public-route-table-assoc" {
  subnet_id      = aws_subnet.public-subnet.id
  route_table_id = aws_route_table.public-route-table.id
}
