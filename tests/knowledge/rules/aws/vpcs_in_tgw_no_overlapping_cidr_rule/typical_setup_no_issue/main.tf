provider "aws" {
  region = "eu-central-1"
}

locals {
  test_description = "TGW - no overlaps (good case)"
  test_name        = "VpcsInTransitGatewayNoOverlappingCidrRule test - use case 1"
}

module "vpc1" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 2.0"

  name = "vpc1"

  cidr = "10.10.0.0/16"

  azs             = ["eu-central-1a"]
  private_subnets = ["10.10.1.0/24"]

  enable_ipv6                                    = true
  private_subnet_assign_ipv6_address_on_creation = true
  private_subnet_ipv6_prefixes                   = [0]
}

module "vpc2" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 2.0"

  name = "vpc2"

  cidr = "10.20.0.0/16"

  azs             = ["eu-central-1a"]
  private_subnets = ["10.20.1.0/24"]

  enable_ipv6 = false
}

resource "aws_ec2_transit_gateway" "tgw" {
  description = "tgw context test"
  amazon_side_asn                 = 64512
  auto_accept_shared_attachments  = "disable"
  default_route_table_association = "enable"
  default_route_table_propagation = "enable"
  dns_support                     = "enable"
  vpn_ecmp_support                = "enable"

}

resource "aws_ec2_transit_gateway_vpc_attachment" "attachment1" {
  transit_gateway_id = aws_ec2_transit_gateway.tgw.id
  vpc_id             = module.vpc1.vpc_id
  dns_support        = "enable"

  subnet_ids = [
    module.vpc1.private_subnets[0]
  ]
}


resource "aws_ec2_transit_gateway_vpc_attachment" "attachment2" {
  transit_gateway_id = aws_ec2_transit_gateway.tgw.id
  vpc_id             = module.vpc2.vpc_id
  dns_support        = "enable"

  subnet_ids = [
    module.vpc2.private_subnets[0]
  ]
}

resource "aws_route" "tgw-route-from-1-to-2" {
  route_table_id         = module.vpc1.default_route_table_id
  destination_cidr_block = module.vpc2.private_subnets_cidr_blocks[0]
  transit_gateway_id     = aws_ec2_transit_gateway.tgw.id
}

resource "aws_route" "tgw-route-from-2-to-1" {
  route_table_id         = module.vpc2.default_route_table_id
  destination_cidr_block = module.vpc1.private_subnets_cidr_blocks[0]
  transit_gateway_id     = aws_ec2_transit_gateway.tgw.id
}
