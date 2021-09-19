provider "aws" {
  region = "eu-west-1"
}

locals {
  test_description = "VPC Peering - routes too permissive, wider than peer VPC, report issue"
  test_name        = "VPC Peering - use case 1"
}

resource "aws_vpc" "vpc1" {
  cidr_block = "10.5.0.0/16"
}

resource "aws_subnet" "subnet1_1" {
  vpc_id = aws_vpc.vpc1.id
  cidr_block = "10.5.10.0/24"
}

resource "aws_subnet" "subnet1_2" {
  vpc_id = aws_vpc.vpc1.id
  cidr_block = "10.5.11.0/24"
}

resource "aws_vpc" "vpc2" {
  cidr_block = "10.7.0.0/16"
}

resource "aws_subnet" "subnet2_1" {
  vpc_id = aws_vpc.vpc2.id
  cidr_block = "10.7.10.0/24"
}

resource "aws_subnet" "subnet2_2" {
  vpc_id = aws_vpc.vpc2.id
  cidr_block = "10.7.11.0/24"
}

module "vpc-peering" {
  source  = "./modules/vpc-peering"

  this_vpc_id = aws_vpc.vpc1.id
  peer_vpc_id = aws_vpc.vpc2.id
}

resource "aws_route_table" "subnet2_1" {
  vpc_id = aws_vpc.vpc2.id
  route {
    cidr_block = "0.0.0.0/0" // This route is too permissive.
    vpc_peering_connection_id = module.vpc-peering.aws_vpc_peering_connection.id
  }
}

resource "aws_route_table_association" "subnet2_1" {
  subnet_id = aws_subnet.subnet2_2.id
  route_table_id = aws_route_table.subnet2_1.id
}