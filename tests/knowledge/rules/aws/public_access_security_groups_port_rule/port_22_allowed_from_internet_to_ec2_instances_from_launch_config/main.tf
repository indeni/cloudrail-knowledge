terraform {
  required_version = ">= 0.12"
}
provider "aws" {
  region = "us-east-1"
}
locals {
  availability_zones = ["us-east-1a", "us-east-1b"]
}

data "aws_ami" "ubuntu" {
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

resource "aws_elb" "web-elb" {
  name = "terraform-example-elb"
  # The same availability zone as our instances
  availability_zones = local.availability_zones
  listener {
    instance_port     = 80
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }
  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    target              = "HTTP:80/"
    interval            = 30
  }
}
resource "aws_autoscaling_group" "web-asg" {
  availability_zones   = local.availability_zones
  name                 = "terraform-example-asg"
  max_size             = 5
  min_size             = 1
  desired_capacity     = 2
  force_delete         = true
  launch_configuration = aws_launch_configuration.web-lc.name
  load_balancers       = [aws_elb.web-elb.name]
  #vpc_zone_identifier = ["${split(",", var.availability_zones)}"]
  tag {
    key                 = "Name"
    value               = "web-asg"
    propagate_at_launch = "true"
  }
}
resource "aws_launch_configuration" "web-lc" {
  name          = "terraform-example-lc"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "m4.large"
  # Security group
  security_groups = [aws_security_group.default.id]
  key_name        = "develop"
}
# Our default security group to access
# the instances over SSH and HTTP
resource "aws_security_group" "default" {
  name        = "terraform_example_sg"
  description = "Used in the terraform"
  # SSH access from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # HTTP access from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}