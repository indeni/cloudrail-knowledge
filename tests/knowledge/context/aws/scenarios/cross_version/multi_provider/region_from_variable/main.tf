variable "region" { type = string }

//provider_"aws" {
//  region = var.region
//}

resource "aws_vpc" "east" {
  cidr_block = "172.27.0.0/16"
  tags = {
    Name = "us-west-1"
  }
}


