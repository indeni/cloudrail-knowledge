provider "aws" {
  region = "us-east-1"
}

module "vpc_module" {
 source        = "./modules/vpc_module"
}

resource "aws_vpc" "east" {
  cidr_block = "172.25.0.0/16"
  tags = {
    Name = "east1"
  }
}