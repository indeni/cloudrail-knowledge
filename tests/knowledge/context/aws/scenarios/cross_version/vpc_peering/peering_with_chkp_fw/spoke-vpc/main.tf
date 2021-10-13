locals {
  admin_subnet           = "81.47.147.15/32"
  environment            = "testing"
  chkp_tag               = "transitvpc"
  spoke_instance_ami     = "ami-0fc61db8544a617ed"
  spoke_instance_type    = "t2.micro"
  spoke1_vpc_cidr_block  = "10.100.0.0/16"
  spoke1_vpc_subnet_cidr = "10.100.10.0/24"
  spoke2_vpc_cidr_block  = "10.200.0.0/16"
  spoke2_vpc_subnet_cidr = "10.200.10.0/24"

  chkp_transit_vpc_cidr_block = "10.60.0.0/16"
}


############################
# SPOKE 1 VPC
############################
module "spoke1_vpc" {
  source                 = "../modules/spoke_vpc"
  name                   = "spoke1_vpc"
  environment            = local.environment
  cidr_block             = local.spoke1_vpc_cidr_block
  subnet_cidr            = local.spoke1_vpc_subnet_cidr
  app_name               = "spoke1"
  provisioning_tag_value = "${local.chkp_tag}-management/${local.chkp_tag}-community"
  instance_image         = local.spoke_instance_ami
  instance_type          = local.spoke_instance_type
  key_name               = var.key_name
  admin_subnet           = local.chkp_transit_vpc_cidr_block
  spoke_service_access   = local.spoke2_vpc_cidr_block
}

############################
# SPOKE 2 VPC
############################
module "spoke2_vpc" {
  source                 = "../modules/spoke_vpc"
  name                   = "spoke2_vpc"
  environment            = local.environment
  cidr_block             = local.spoke2_vpc_cidr_block
  subnet_cidr            = local.spoke2_vpc_subnet_cidr
  app_name               = "spoke2"
  provisioning_tag_value = "${local.chkp_tag}-management/${local.chkp_tag}-community"
  instance_image         = local.spoke_instance_ami
  instance_type          = local.spoke_instance_type
  key_name               = var.key_name
  admin_subnet           = local.chkp_transit_vpc_cidr_block
  spoke_service_access   = local.spoke1_vpc_cidr_block
}
