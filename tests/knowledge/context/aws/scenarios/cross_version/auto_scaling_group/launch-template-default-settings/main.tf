
resource "aws_autoscaling_group" "test-autoscaling-group" {
  name                      = "test-autoscaling-group"
  max_size                  = 5
  min_size                  = 2
  vpc_zone_identifier       = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]

  launch_template {
    id      = aws_launch_template.test-launch-template.id
    version = "$Latest"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_launch_template" "test-launch-template" {
  name = "test-launch-template"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}

resource "aws_vpc" "main" {
  cidr_block = "172.16.0.0/16"
}

resource "aws_subnet" "private-subnet-1" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "172.16.100.0/24"
  map_public_ip_on_launch = true
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-subnet-1"
  }
}

resource "aws_subnet" "private-subnet-2" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "172.16.101.0/24"
  map_public_ip_on_launch = false
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-subnet-2"
  }
}

resource "aws_security_group" "allow-http" {
  description = "allow http"
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