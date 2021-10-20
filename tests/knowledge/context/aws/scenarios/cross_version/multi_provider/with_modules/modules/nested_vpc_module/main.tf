//provider_"aws" {
//  region = "us-west-1"
//  alias = "west"
//}

resource "aws_vpc" "east" {
  cidr_block = "172.27.0.0/16"
  tags = {
    Name = "nested_vpc_module-east2"
  }
}

resource "aws_vpc" "west" {
  provider = aws.west
  cidr_block = "172.28.0.0/16"
  tags = {
    Name = "nested_vpc_module-west"
  }
}