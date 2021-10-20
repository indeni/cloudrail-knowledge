
locals {
  test-description = "EC2 required http tokens"
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

resource "aws_instance" "default" {
  ami = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
    tags = {
    Name = "my_ec2"
  }
  metadata_options {
    http_tokens = "required"
    http_put_response_hop_limit = 2
    http_endpoint = "enabled"
  }
}