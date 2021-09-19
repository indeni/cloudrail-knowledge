###################
# Local variables
##################
locals {
  public_subnet_router  = cidrhost(data.aws_subnet.public.cidr_block, 1)
  private_subnet_router = cidrhost(data.aws_subnet.private.cidr_block, 1)
  sic_key_b64           = base64encode(var.sic_key)
  use_auto_provision    = var.management_server != "" || var.configuration_template != ""
  auto_provision_key    = local.use_auto_provision ? "x-chkp-tags+" : "ignored-tag-key"
  auto_provision_value  = local.use_auto_provision ? "management=${var.management_server}+template=${var.configuration_template}+ip-address=${var.control_gateway_over_private_or_public_address}" : "ignored-tag-value"
}

data "aws_subnet" "public" {
  id = var.public_subnet_id
}

data "aws_subnet" "private" {
  id = var.private_subnet_id
}

####################################
# CLOUDGUARD GATEWAY NACL - Public
####################################
resource "aws_network_acl_rule" "public_inbound" {
  network_acl_id = var.public_nacl
  egress         = false
  rule_number    = 100
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 65535
}

resource "aws_network_acl_rule" "public_outbound" {
  network_acl_id = var.public_nacl
  egress         = true
  rule_number    = 100
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 65535
}

####################################
# CLOUDGUARD GATEWAY NACL - Private
####################################
resource "aws_network_acl_rule" "private_inbound" {
  network_acl_id = var.private_nacl
  egress         = false
  rule_number    = 100
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = var.chkp_mgmt_subnet
  from_port      = 0
  to_port        = 65535
}

resource "aws_network_acl_rule" "private_outbound" {
  network_acl_id = var.private_nacl
  egress         = true
  rule_number    = 100
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = var.chkp_mgmt_subnet
  from_port      = 0
  to_port        = 65535
}

###############################################################
# CLOUDGUARD GATEWAY SECURITY GROUP - Public interfaces (eth0)
###############################################################
resource "aws_security_group" "public" {
  description = "SG for CloudGuard Gateway public interface"
  vpc_id      = var.vpc_id
  tags = {
    Name        = "${var.name}-public-cg_gateway"
    Environment = var.environment
  }
}

resource "aws_security_group_rule" "public_inbound" {
  security_group_id = aws_security_group.public.id
  type              = "ingress"
  cidr_blocks       = ["0.0.0.0/0"]
  protocol          = "-1"
  from_port         = 0
  to_port           = 0
}

resource "aws_security_group_rule" "public_outbound" {
  security_group_id = aws_security_group.public.id
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
  protocol          = "-1"
  from_port         = 0
  to_port           = 0
}

###############################################################
# CLOUDGUARD GATEWAY SECURITY GROUP - Private interfaces (eth1)
###############################################################
resource "aws_security_group" "private" {
  description = "SG for CloudGuard Gateway private interface"
  vpc_id      = var.vpc_id
  tags = {
    Name        = "${var.name}-private-cg_gateway"
    Environment = var.environment
  }
}

resource "aws_security_group_rule" "inbound_18191_18192" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18191
  to_port                  = 18192
}

resource "aws_security_group_rule" "inbound_18211" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18211
  to_port                  = 18211
}

resource "aws_security_group_rule" "inbound_256" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 256
  to_port                  = 256
}

resource "aws_security_group_rule" "inbound_18202" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18202
  to_port                  = 18202
}

resource "aws_security_group_rule" "inbound_18183" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18183
  to_port                  = 18183
}

resource "aws_security_group_rule" "inbound_18208" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18208
  to_port                  = 18208
}

resource "aws_security_group_rule" "inbound_22" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 22
  to_port                  = 22
}

resource "aws_security_group_rule" "inbound_443" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 443
  to_port                  = 443
}

resource "aws_security_group_rule" "inbound_69" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "udp"
  from_port                = 69
  to_port                  = 69
}

resource "aws_security_group_rule" "inbound_21" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 21
  to_port                  = 21
}

resource "aws_security_group_rule" "inbound_389" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 389
  to_port                  = 389
}

resource "aws_security_group_rule" "inbound_636" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 636
  to_port                  = 636
}

resource "aws_security_group_rule" "inbound_123" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "udp"
  from_port                = 123
  to_port                  = 123
}

resource "aws_security_group_rule" "inbound_161" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "udp"
  from_port                = 161
  to_port                  = 161
}

resource "aws_security_group_rule" "inbound_53" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "udp"
  from_port                = 53
  to_port                  = 53
}

resource "aws_security_group_rule" "inbound_18187" {
  security_group_id        = aws_security_group.private.id
  type                     = "ingress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18187
  to_port                  = 18187
}

resource "aws_security_group_rule" "outbound_257" {
  security_group_id        = aws_security_group.private.id
  type                     = "egress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 257
  to_port                  = 257
}

resource "aws_security_group_rule" "outbound_18191_18192" {
  security_group_id        = aws_security_group.private.id
  type                     = "egress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18191
  to_port                  = 18192
}

resource "aws_security_group_rule" "outbound_18210_18211" {
  security_group_id        = aws_security_group.private.id
  type                     = "egress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18210
  to_port                  = 18211
}

resource "aws_security_group_rule" "outbound_18221" {
  security_group_id        = aws_security_group.private.id
  type                     = "egress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18221
  to_port                  = 18221
}

resource "aws_security_group_rule" "outbound_18264" {
  security_group_id        = aws_security_group.private.id
  type                     = "egress"
  source_security_group_id = var.chkp_management_security_group
  protocol                 = "tcp"
  from_port                = 18264
  to_port                  = 18264
}

########################################
# CLOUDGUARD GATEWAY NETWORK INTERFACES
########################################
resource "aws_network_interface" "public" {
  description       = "External"
  subnet_id         = var.public_subnet_id
  security_groups   = [aws_security_group.public.id]
  source_dest_check = false
}

resource "aws_network_interface" "private" {
  description       = "Internal"
  subnet_id         = var.private_subnet_id
  security_groups   = [aws_security_group.private.id]
  source_dest_check = false
  tags = {
    x-chkp-topology      = "internal"
    x-chkp-anti-spoofing = "false"
  }
}

########################################
# CLOUDGUARD GATEWAY INSTANCE
########################################
resource "aws_instance" "gateway" {
  ami           = var.image_id
  instance_type = var.instance_type
  key_name      = var.key_name
  network_interface {
    device_index         = "0"
    network_interface_id = aws_network_interface.public.id
  }
  network_interface {
    device_index         = "1"
    network_interface_id = aws_network_interface.private.id
  }
  user_data = <<EOF
    #!/bin/bash
    echo
  EOF
  tags = {
    Name                       = var.gateway_name
    (local.auto_provision_key) = local.auto_provision_value
    x-chkp-ip-address          = element(tolist(aws_network_interface.private.private_ips), 0)
  }
}

####################
# Public IP address
####################
resource "aws_eip" "public" {
  vpc               = true
  network_interface = aws_network_interface.public.id
}
