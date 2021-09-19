/**
* IMPORTANT:
* This originally created CHKP FWs, but we switched to
* created Ubuntu instances so that the code wouldn't need to subscribe
* to CloudGuard.
*/
data "aws_region" "current" {
  name = "us-east-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

locals {
  admin_subnet          = ["81.47.147.15/32"]
  password_hash         = "$1$7hYaKWg9$NNjkmJsVkUix5eKd9wYs20" # Password: In.de.ni.2020
  gateway_instance_type = "c5.large"
  mgmt_instance_type    = "m5.large"
  sic_key               = "abcd1234"
  chkp_tag              = "transitvpc"
  environment           = "testing"
  asn                   = 65000
  gateway_image_id      = data.aws_ami.ubuntu.id
  mgmt_image_id         = data.aws_ami.ubuntu.id

  # IP Addressing
  chkp_mgmt_vpc_cidr_block          = "10.50.0.0/16"
  chkp_mgmt_vpc_public_subnet_1     = "10.50.1.0/24"
  chkp_transit_vpc_cidr_block       = "10.60.0.0/16"
  chkp_transit_vpc_public_subnet_1  = "10.60.1.0/24"
  chkp_transit_vpc_public_subnet_2  = "10.60.2.0/24"
  chkp_transit_vpc_private_subnet_1 = "10.60.10.0/24"
  chkp_transit_vpc_private_subnet_2 = "10.60.20.0/24"

}

############################
# CHECKPOINT MANAGEMENT VPC
############################
module "mgmt_vpc" {
  source                 = "../modules/vpc"
  create_igw             = true
  create_public_subnets  = true
  create_private_subnets = false
  name                   = "chkp_mgmt_vpc"
  environment            = local.environment
  cidr_block             = local.chkp_mgmt_vpc_cidr_block
  az_public_subnet = {
    (local.chkp_mgmt_vpc_public_subnet_1) = { az = "us-east-1a", app = "" }
  }
}

############################
# CHECKPOINT TRANSIT VPC
############################
module "transit_vpc" {
  source                 = "../modules/vpc"
  create_igw             = true
  create_public_subnets  = true
  create_private_subnets = true
  name                   = "chkp_transit_vpc"
  environment            = local.environment
  cidr_block             = local.chkp_transit_vpc_cidr_block
  az_public_subnet = {
    (local.chkp_transit_vpc_public_subnet_1) = { az = "us-east-1a", app = "A" }
    (local.chkp_transit_vpc_public_subnet_2) = { az = "us-east-1b", app = "B" }
  }
  az_private_subnet = {
    (local.chkp_transit_vpc_private_subnet_1) = { az = "us-east-1a", app = "A" }
    (local.chkp_transit_vpc_private_subnet_2) = { az = "us-east-1b", app = "B" }
  }
}

########################################
# VPC PEERING: mgmt_vpc and transit_vpc
########################################
resource "aws_vpc_peering_connection" "peering" {
  vpc_id      = "${module.mgmt_vpc.vpc_id}"
  peer_vpc_id = "${module.transit_vpc.vpc_id}"
  auto_accept = true
}

resource "aws_vpc_peering_connection_options" "peering" {
  vpc_peering_connection_id = "${aws_vpc_peering_connection.peering.id}"
  accepter {
    allow_remote_vpc_dns_resolution = true
  }
  requester {
    allow_remote_vpc_dns_resolution = true
  }
}

resource "aws_route" "mgmt_to_gwA" {
  route_table_id            = module.mgmt_vpc.public_route_table
  destination_cidr_block    = local.chkp_transit_vpc_private_subnet_1
  vpc_peering_connection_id = aws_vpc_peering_connection.peering.id
}

resource "aws_route" "mgmt_to_gwB" {
  route_table_id            = module.mgmt_vpc.public_route_table
  destination_cidr_block    = local.chkp_transit_vpc_private_subnet_2
  vpc_peering_connection_id = aws_vpc_peering_connection.peering.id
}

resource "aws_route" "gws_to_mgmt" {
  route_table_id            = module.transit_vpc.private_route_table
  destination_cidr_block    = local.chkp_mgmt_vpc_public_subnet_1
  vpc_peering_connection_id = aws_vpc_peering_connection.peering.id
}

###############################
# CHECKPOINT MANAGEMENT SERVER
###############################
module "mgmt" {
  source                = "../modules/cloudguard_management"
  name                  = "${local.chkp_tag}-management"
  vpc_id                = module.mgmt_vpc.vpc_id
  subnet_id             = module.mgmt_vpc.public_subnets[0]
  public_nacl           = module.mgmt_vpc.public_nacl[0]
  instance_type         = local.mgmt_instance_type
  image_id              = local.mgmt_image_id
  management_name       = "chkp-mgmt"
  hostname              = "chkp-mgmt"
  password_hash         = local.password_hash
  allow_upload_download = false
  admin_subnet          = local.admin_subnet
  gateways_addresses    = [local.chkp_transit_vpc_private_subnet_1, local.chkp_transit_vpc_private_subnet_2]
  sic_key               = local.sic_key
  chkp_tag              = "transitvpc"
  key_name = var.key_name
}

#######################
# CHECKPOINT GATEWAY A
#######################
module "cloudguard_gateway_A" {
  source                                         = "../modules/cloudguard_gateway"
  name                                           = "${local.chkp_tag}-gatewayA"
  environment                                    = local.environment
  vpc_id                                         = module.transit_vpc.vpc_id
  public_subnet_id                               = module.transit_vpc.public_subnets[0]
  private_subnet_id                              = module.transit_vpc.private_subnets[0]
  public_nacl                                    = module.transit_vpc.public_nacl[0]
  private_nacl                                   = module.transit_vpc.private_nacl[0]
  chkp_mgmt_subnet                               = local.chkp_mgmt_vpc_public_subnet_1
  chkp_management_security_group                 = module.mgmt.chkp_management_security_group
  gateway_name                                   = "gatewayA"
  image_id                                       = local.gateway_image_id
  instance_type                                  = local.gateway_instance_type
  key_name                                       = var.key_name
  shell                                          = "/etc/cli.sh"
  password_hash                                  = local.password_hash
  asn                                            = local.asn
  sic_key                                        = local.sic_key
  allow_upload_download                          = false
  management_server                              = "${local.chkp_tag}-management"
  configuration_template                         = "${local.chkp_tag}-template"
  control_gateway_over_private_or_public_address = "private"
}

#######################
# CHECKPOINT GATEWAY B
#######################
module "cloudguard_gateway_B" {
  source                                         = "../modules/cloudguard_gateway"
  name                                           = "${local.chkp_tag}-gatewayB"
  environment                                    = local.environment
  vpc_id                                         = module.transit_vpc.vpc_id
  public_subnet_id                               = module.transit_vpc.public_subnets[1]
  private_subnet_id                              = module.transit_vpc.private_subnets[1]
  public_nacl                                    = module.transit_vpc.public_nacl[0]
  private_nacl                                   = module.transit_vpc.private_nacl[0]
  chkp_mgmt_subnet                               = local.chkp_mgmt_vpc_public_subnet_1
  chkp_management_security_group                 = module.mgmt.chkp_management_security_group
  gateway_name                                   = "gatewayB"
  image_id                                       = local.gateway_image_id
  instance_type                                  = local.gateway_instance_type
  key_name                                       = var.key_name
  shell                                          = "/etc/cli.sh"
  password_hash                                  = local.password_hash
  asn                                            = local.asn
  sic_key                                        = local.sic_key
  allow_upload_download                          = false
  management_server                              = "${local.chkp_tag}-management"
  configuration_template                         = "${local.chkp_tag}-template"
  control_gateway_over_private_or_public_address = "private"
}
