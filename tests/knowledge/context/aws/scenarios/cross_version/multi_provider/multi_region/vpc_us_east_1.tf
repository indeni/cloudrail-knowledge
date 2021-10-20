//provider_"aws" {
//  region = "us-east-1"
//}

resource "aws_vpc" "east" {
  cidr_block = "172.27.0.0/16"
  tags = {
    Name = "us-east-1"
  }
}


