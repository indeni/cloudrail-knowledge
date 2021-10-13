########################
# VPC
########################
resource "aws_vpc" "vpc" {
  cidr_block           = var.cidr_block
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name        = "${var.name}"
    Environment = var.environment
  }
}

# This special resource is used in order to manage the default Network ACL created with the VPC.
# Terraform will automatically delete the ALLOW rules of this default NACL. 
resource "aws_default_network_acl" "default" {
  default_network_acl_id = aws_vpc.vpc.default_network_acl_id
}

# This special resource is used in order to manage the default Security Group created with the VPC.
# Terraform will automatically delete the ALLOW rules of this Security Group. 
resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.vpc.id
}

########################
# INTERNET GATEWAY
########################
resource "aws_internet_gateway" "igw" {
  count  = var.create_igw ? 1 : 0
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name        = "${var.name}"
    Environment = var.environment
  }
}

########################
# PUBLIC SUBNETS
########################
resource "aws_subnet" "public" {
  for_each                = var.create_public_subnets ? var.az_public_subnet : {}
  cidr_block              = each.key
  vpc_id                  = aws_vpc.vpc.id
  availability_zone       = each.value["az"]
  map_public_ip_on_launch = true
  tags = {
    Name        = format("%s-public%s", var.name, each.value["app"])
    Environment = var.environment
  }
}

##########################
# PUBLIC SUBNETS ROUTING
##########################
resource "aws_route_table" "public" {
  count  = var.create_public_subnets ? 1 : 0
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name        = "${var.name}-public"
    Environment = var.environment
  }
}

resource "aws_route" "public" {
  count                  = var.create_public_subnets ? 1 : 0
  route_table_id         = aws_route_table.public[0].id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw[0].id
}

resource "aws_route_table_association" "public" {
  count          = var.create_public_subnets ? length(var.az_public_subnet) : 0
  subnet_id      = element(values(aws_subnet.public)[*].id, count.index)
  route_table_id = aws_route_table.public[0].id
}

##########################
# PUBLIC NETWORK ACL
##########################
resource "aws_network_acl" "public" {
  count      = var.create_public_subnets ? 1 : 0
  vpc_id     = aws_vpc.vpc.id
  subnet_ids = values(aws_subnet.public)[*].id
  tags = {
    Name        = format("%s-public", var.name)
    Environment = var.environment
  }
}

########################
# PRIVATE SUBNETS
########################
resource "aws_subnet" "private" {
  for_each          = var.create_private_subnets ? var.az_private_subnet : {}
  cidr_block        = each.key
  vpc_id            = aws_vpc.vpc.id
  availability_zone = each.value["az"]
  tags = {
    Name        = format("%s-private%s", var.name, each.value["app"])
    Environment = var.environment
  }
}

##########################
# PRIVATE SUBNETS ROUTING
##########################
resource "aws_route_table" "private" {
  count  = var.create_private_subnets ? 1 : 0
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name        = "${var.name}-private"
    Environment = var.environment
  }
}

resource "aws_route_table_association" "private" {
  count          = var.create_private_subnets ? length(var.az_private_subnet) : 0
  subnet_id      = element(values(aws_subnet.private)[*].id, count.index)
  route_table_id = aws_route_table.private[0].id
}

##########################
# PRIVATE NETWORK ACLs
##########################
resource "aws_network_acl" "private" {
  count      = var.create_private_subnets ? 1 : 0
  vpc_id     = aws_vpc.vpc.id
  subnet_ids = values(aws_subnet.private)[*].id
  tags = {
    Name        = format("%s-private", var.name)
    Environment = var.environment
  }
}
