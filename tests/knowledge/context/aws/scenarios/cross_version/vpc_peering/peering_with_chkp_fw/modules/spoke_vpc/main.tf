########################
# VPC
########################
resource "aws_vpc" "vpc" {
  cidr_block           = var.cidr_block
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name         = "${var.name}"
    Environment  = var.environment
    "x-chkp-vpn" = var.provisioning_tag_value
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
# SUBNET
########################
resource "aws_subnet" "subnet" {
  cidr_block = var.subnet_cidr
  vpc_id     = aws_vpc.vpc.id
  tags = {
    Name        = var.app_name
    Environment = var.environment
  }
}

##########################
# NETWORK ACL
##########################
resource "aws_network_acl" "nacl" {
  vpc_id     = aws_vpc.vpc.id
  subnet_ids = [aws_subnet.subnet.id]
  tags = {
    Name        = var.app_name
    Environment = var.environment
  }
}

resource "aws_network_acl_rule" "inbound_ssh_from_other_spoke" {
  network_acl_id = aws_network_acl.nacl.id
  egress         = false
  rule_number    = 100
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = var.spoke_service_access
  from_port      = 22
  to_port        = 22
}

resource "aws_network_acl_rule" "inbound_ssh_from_gws" {
  network_acl_id = aws_network_acl.nacl.id
  egress         = false
  rule_number    = 101
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = var.admin_subnet
  from_port      = 22
  to_port        = 22
}

resource "aws_network_acl_rule" "inbound_ephemeral" {
  network_acl_id = aws_network_acl.nacl.id
  egress         = false
  rule_number    = 102
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 1024
  to_port        = 65535
}

resource "aws_network_acl_rule" "egress_ssh" {
  network_acl_id = aws_network_acl.nacl.id
  egress         = true
  rule_number    = 100
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = var.spoke_service_access
  from_port      = 22
  to_port        = 22
}

resource "aws_network_acl_rule" "egress_http" {
  network_acl_id = aws_network_acl.nacl.id
  egress         = true
  rule_number    = 101
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 80
  to_port        = 80
}

resource "aws_network_acl_rule" "egress_https" {
  network_acl_id = aws_network_acl.nacl.id
  egress         = true
  rule_number    = 102
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 443
  to_port        = 443
}

resource "aws_network_acl_rule" "egress_ephemeral" {
  network_acl_id = aws_network_acl.nacl.id
  egress         = true
  rule_number    = 103
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 1024
  to_port        = 65535
}

#################
# SECURITY GROUP
#################
resource "aws_security_group" "app" {
  description = "SG for internal App"
  vpc_id      = aws_vpc.vpc.id
  tags = {
    Name        = "${var.name}-sg"
    Environment = var.environment
  }
}

resource "aws_security_group_rule" "inbound_ssh" {
  security_group_id = aws_security_group.app.id
  type              = "ingress"
  cidr_blocks       = [var.admin_subnet, var.spoke_service_access]
  protocol          = "tcp"
  from_port         = 22
  to_port           = 22
}

resource "aws_security_group_rule" "outbound_http" {
  security_group_id = aws_security_group.app.id
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
  protocol          = "tcp"
  from_port         = 80
  to_port           = 80
}

resource "aws_security_group_rule" "outbound_https" {
  security_group_id = aws_security_group.app.id
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
  protocol          = "tcp"
  from_port         = 443
  to_port           = 443
}

resource "aws_security_group_rule" "outbound_ssh" {
  security_group_id = aws_security_group.app.id
  type              = "egress"
  cidr_blocks       = [var.spoke_service_access]
  protocol          = "tcp"
  from_port         = 22
  to_port           = 22
}

#################
# INSTANCE APP
#################
resource "aws_instance" "app" {
  ami                    = var.instance_image
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = aws_subnet.subnet.id
  vpc_security_group_ids = [aws_security_group.app.id]
  tags = {
    Name        = "${var.name}"
    Environment = var.environment
  }
}
