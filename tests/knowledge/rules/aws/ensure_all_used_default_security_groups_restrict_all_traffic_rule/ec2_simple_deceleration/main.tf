# Test case: resource (ec2) use default sg in default VPC, use default sg
# Expected: alert on the use of default sg

provider "aws" {
  region = "eu-west-2"
}

resource "aws_instance" "ec2" {
  ami = "ami-07cda0db070313c52"
  instance_type = "t2.micro"
  tags = {
    Name = "Integration test - use case 1"
  }
}
