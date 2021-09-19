//provider_"aws" {
//  region = "us-west-1"
//  alias = "west"
//}

resource "aws_vpc" "west" {
  provider = aws.west
  cidr_block = "172.27.0.0/16"
  tags = {
    Name = "us-west-1"
  }
}

