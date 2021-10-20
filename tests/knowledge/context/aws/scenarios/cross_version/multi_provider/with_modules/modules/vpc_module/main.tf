//provider_"aws" {
//  region = "us-east-2"
//}

module "nested_vpc_module" {
 source        = "../nested_vpc_module"
}

resource "aws_vpc" "east" {
  cidr_block = "172.24.0.0/16"
  tags = {
    Name = "vpc_module-east2"
  }
}