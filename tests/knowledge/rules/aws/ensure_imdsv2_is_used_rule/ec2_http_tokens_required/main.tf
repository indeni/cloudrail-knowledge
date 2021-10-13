provider "aws" {
  region = "us-east-1"
}

locals {
  test_name = "test http_tokens state - required"
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

resource "aws_instance" "t2-instance" {
  ami = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  metadata_options {
    http_endpoint = "enabled"
    http_put_response_hop_limit = 1
    http_tokens = "required"
  }
}
