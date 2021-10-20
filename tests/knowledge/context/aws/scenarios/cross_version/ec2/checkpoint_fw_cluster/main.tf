// This is a tricky one:
// The EC2s are created via a launch config used by an autoscaling group.
// There's no direct reference to aws_instance.

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true

}

data "aws_ami" "chkpfw" {
  most_recent = true

  filter {
    name   = "name"
    values = ["Check Point CloudGuard IaaS BYOL*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["679593333241"] # Canonical
}

resource "aws_security_group" "permissive_security_group" {
  name = "permissive_security_group"
  vpc_id = module.vpc.vpc_id
  ingress {
    from_port = 0
    protocol = "-1"
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "permissive_security_group"
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

resource "aws_launch_configuration" "launchconfig" {
  associate_public_ip_address = true
  image_id = data.aws_ami.ubuntu.id   // = data.aws_ami.chkpfw.id // Note, NOT using the chkpfw AMI because that requires accepting terms in the marketplace, which cannot be automated
  security_groups = [aws_security_group.permissive_security_group.id]
  instance_type = "t2.micro"
  user_data = "#!/bin/bash" // there was more in the cloudformation template, but truncated that
}

resource "aws_autoscaling_group" "gatewaygrp" {
  name = "chkp_fws"
  max_size = 5
  min_size = 1
  vpc_zone_identifier = module.vpc.public_subnets
  launch_configuration = aws_launch_configuration.launchconfig.name
}

resource "aws_autoscaling_policy" "scaleup" {
  name = "scaleup"
  adjustment_type = "ChangeInCapacity"
  autoscaling_group_name = aws_autoscaling_group.gatewaygrp.name
  cooldown = 300
  scaling_adjustment = 1
}

resource "aws_autoscaling_policy" "scaledown" {
  name = "scaledown"
  adjustment_type = "ChangeInCapacity"
  autoscaling_group_name = aws_autoscaling_group.gatewaygrp.name
  cooldown = 300
  scaling_adjustment = -1
}
