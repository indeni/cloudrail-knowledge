variable "region" { type = string }

//provider_"aws" {
//  region = var.region
//  alias = "west"
//}

resource "aws_vpc" "east" {
  cidr_block = "172.27.0.0/16"
  tags = {
    Name = "east"
  }
}

resource "aws_vpc" "west" {
  provider = aws.west
  cidr_block = "172.28.0.0/16"
  tags = {
    Name = "west"
  }
}