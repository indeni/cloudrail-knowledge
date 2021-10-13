
resource "aws_autoscaling_group" "test-autoscaling-group" {
  name                      = "test-autoscaling-group"
  max_size                  = 5
  min_size                  = 2
  vpc_zone_identifier       = [aws_subnet.private-subnet.id]

  launch_template {
    id      = aws_launch_template.test-launch-template.id
    version = "$Latest"
  }

  tag {
    key                 = "foo"
    value               = "bar"
    propagate_at_launch = true
  }

  timeouts {
    delete = "15m"
  }

  tag {
    key                 = "lorem"
    value               = "ipsum"
    propagate_at_launch = false
  }
}

data "aws_ami" "ubuntu-ami" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_launch_template" "test-launch-template" {
  name_prefix   = "test-launch-template"
  image_id      = data.aws_ami.ubuntu-ami.id
  instance_type = "t2.micro"

  network_interfaces {
    security_groups = [aws_security_group.allow-http.id]
    subnet_id = aws_subnet.private-subnet.id
  }
}

resource "aws_vpc" "main" {
  cidr_block = "192.168.100.0/24"
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "192.168.100.128/25"
  map_public_ip_on_launch = true

  tags = {
    Name = "private-subnet"
  }
}

resource "aws_security_group" "allow-http" {
  description = "allow http"
  vpc_id     = aws_vpc.main.id
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

