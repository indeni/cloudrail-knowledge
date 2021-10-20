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

/**
This requires vpc1 and vpc2 to exist. If they don't yet, you'll get an error.
So run apply first with  -target aws_vpc.vpc1 -target aws_vpc.vpc2 -target aws_subnet.subnet1_1 -target aws_subnet.subnet1_2 -target aws_subnet.subnet2_1 -target aws_subnet.subnet2_2

Also, if you get:
Error: error modifying VPC Peering Connection (pcx-0e4446169b775fc60) Options: OperationNotPermitted: Peering pcx-0e4446169b775fc60 is not active. Peering options can be added only to active peerings.

Then go into the Console of AWS -> VPC -> VPC Peering and approve the peering request.
*/
module "vpc-peering" {
  source  = "./modules/vpc-peering"

  this_vpc_id = aws_vpc.vpc1.id
  peer_vpc_id = aws_vpc.vpc2.id
  auto_accept_peering = true
}

resource "aws_route_table" "subnet2_1" {
  vpc_id = aws_vpc.vpc2.id
  route {
    cidr_block = "0.0.0.0/0"
    vpc_peering_connection_id = module.vpc-peering.aws_vpc_peering_connection.id
  }
}

resource "aws_route_table_association" "subnet2_1" {
  subnet_id = aws_subnet.subnet2_2.id
  route_table_id = aws_route_table.subnet2_1.id
}