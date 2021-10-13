data "aws_region" "current" {}


##############################
# CLOUDGUARD MGMT SERVER NACL 
##############################
resource "aws_network_acl_rule" "inbound_ephemeral" {
  network_acl_id = var.public_nacl
  egress         = false
  rule_number    = 99
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 1024
  to_port        = 65535
}

resource "aws_network_acl_rule" "inbound_admin_22" {
  network_acl_id = var.public_nacl
  egress         = false
  rule_number    = 100
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = var.admin_subnet[0]
  from_port      = 22
  to_port        = 22
}

resource "aws_network_acl_rule" "inbound_admin_443" {
  network_acl_id = var.public_nacl
  egress         = false
  rule_number    = 101
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = var.admin_subnet[0]
  from_port      = 443
  to_port        = 443
}

resource "aws_network_acl_rule" "inbound_admin_18190" {
  network_acl_id = var.public_nacl
  egress         = false
  rule_number    = 102
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = var.admin_subnet[0]
  from_port      = 18190
  to_port        = 18190
}

resource "aws_network_acl_rule" "inbound_admin_19009" {
  network_acl_id = var.public_nacl
  egress         = false
  rule_number    = 103
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = var.admin_subnet[0]
  from_port      = 19009
  to_port        = 19009
}

resource "aws_network_acl_rule" "inbound_transit_gw_A" {
  network_acl_id = var.public_nacl
  egress         = false
  rule_number    = 200
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = var.gateways_addresses[0]
  from_port      = 0
  to_port        = 65535
}

resource "aws_network_acl_rule" "inbound_transit_gw_B" {
  network_acl_id = var.public_nacl
  egress         = false
  rule_number    = 201
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = var.gateways_addresses[1]
  from_port      = 0
  to_port        = 65535
}

resource "aws_network_acl_rule" "outbound" {
  network_acl_id = var.public_nacl
  egress         = true
  rule_number    = 104
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 65535
}

#######################################
# CLOUDGUARD MANAGEMENT SECURITY GROUP
#######################################
resource "aws_security_group" "management" {
  description = "SG for Checkpoint Cloudguard Management Server"
  vpc_id      = var.vpc_id
  tags = {
    Name = "${var.name}-chkp-mgmt"
  }
}

#############################################
# CLOUDGUARD MANAGEMENT SECURITY GROUP RULES
#############################################
resource "aws_security_group_rule" "tcp_257" {
  security_group_id = aws_security_group.management.id
  type              = "ingress"
  cidr_blocks       = var.gateways_addresses
  protocol          = "tcp"
  from_port         = 257
  to_port           = 257
}

resource "aws_security_group_rule" "tcp_18191_18192" {
  security_group_id = aws_security_group.management.id
  type              = "ingress"
  cidr_blocks       = var.gateways_addresses
  protocol          = "tcp"
  from_port         = 18191
  to_port           = 18192
}

resource "aws_security_group_rule" "tcp_18210_18211" {
  security_group_id = aws_security_group.management.id
  type              = "ingress"
  cidr_blocks       = var.gateways_addresses
  protocol          = "tcp"
  from_port         = 18210
  to_port           = 18211
}

resource "aws_security_group_rule" "tcp_18221" {
  security_group_id = aws_security_group.management.id
  type              = "ingress"
  cidr_blocks       = var.gateways_addresses
  protocol          = "tcp"
  from_port         = 18221
  to_port           = 18221
}

resource "aws_security_group_rule" "tcp_18264" {
  security_group_id = aws_security_group.management.id
  type              = "ingress"
  cidr_blocks       = var.gateways_addresses
  protocol          = "tcp"
  from_port         = 18264
  to_port           = 18264
}

resource "aws_security_group_rule" "tcp_22" {
  security_group_id = aws_security_group.management.id
  type              = "ingress"
  cidr_blocks       = var.admin_subnet
  protocol          = "tcp"
  from_port         = 22
  to_port           = 22
}

resource "aws_security_group_rule" "tcp_443" {
  security_group_id = aws_security_group.management.id
  type              = "ingress"
  cidr_blocks       = var.admin_subnet
  protocol          = "tcp"
  from_port         = 443
  to_port           = 443
}

resource "aws_security_group_rule" "tcp_18190" {
  security_group_id = aws_security_group.management.id
  type              = "ingress"
  cidr_blocks       = var.admin_subnet
  protocol          = "tcp"
  from_port         = 18190
  to_port           = 18190
}

resource "aws_security_group_rule" "tcp_19009" {
  security_group_id = aws_security_group.management.id
  type              = "ingress"
  cidr_blocks       = var.admin_subnet
  protocol          = "tcp"
  from_port         = 19009
  to_port           = 19009
}

resource "aws_security_group_rule" "outbound" {
  security_group_id = aws_security_group.management.id
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
  protocol          = "-1"
  from_port         = 0
  to_port           = 65535
}

#################################
# CLOUDGUARD MANAGEMENT IAM ROLE
#################################
data "aws_iam_policy_document" "management-assume" {
  version = "2012-10-17"
  statement {
    sid     = "AssumeRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "management-policy" {
  version = "2012-10-17"
  statement {
    sid    = "ChkpManagementServerReadCreatePermissions"
    effect = "Allow"
    actions = [
      "ec2:DescribeCustomerGateways",
      "ec2:CreateCustomerGateway",
      "ec2:DeleteCustomerGateway",
      "ec2:DescribeRouteTables",
      "ec2:EnableVgwRoutePropagation",
      "ec2:DisableVgwRoutePropagation",
      "ec2:CreateVpnGateway",
      "ec2:AttachVpnGateway",
      "ec2:DetachVpnGateway",
      "ec2:DeleteVpnGateway",
      "ec2:CreateVpnConnection",
      "ec2:DeleteVpnConnection",
      "ec2:DescribeTransitGateways",
      "ec2:DescribeTransitGatewayRouteTables",
      "ec2:DescribeTransitGatewayAttachments",
      "ec2:AssociateTransitGatewayRouteTable",
      "ec2:DisassociateTransitGatewayRouteTable",
      "ec2:EnableTransitGatewayRouteTablePropagation",
      "ec2:DisableTransitGatewayRouteTablePropagation",
      "ec2:GetTransitGatewayAttachmentPropagations",
      "ec2:DescribeInstances",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DescribeSubnets",
      "ec2:DescribeVpcs",
      "ec2:DescribeVpnGateways",
      "ec2:DescribeVpnConnections",
      "ec2:DescribeSecurityGroups",
      "elasticloadbalancing:DescribeLoadBalancers",
      "elasticloadbalancing:DescribeTags",
      "elasticloadbalancing:DescribeListeners",
      "elasticloadbalancing:DescribeTargetGroups",
      "elasticloadbalancing:DescribeRules",
      "elasticloadbalancing:DescribeTargetHealth",
      "autoscaling:DescribeAutoScalingGroups",
      "cloudformation:CreateStack",
      "cloudformation:DeleteStack",
      "cloudformation:DescribeStacks",
      "cloudformation:DescribeStackResources",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "management" {
  policy = data.aws_iam_policy_document.management-policy.json
}

resource "aws_iam_role_policy_attachment" "management" {
  role       = aws_iam_role.management.name
  policy_arn = aws_iam_policy.management.arn
}

resource "aws_iam_role" "management" {
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.management-assume.json
}

#########################################
# CLOUDGUARD MANAGEMENT INSTANCE PROFILE
#########################################
resource "aws_iam_instance_profile" "management" {
  role = aws_iam_role.management.name
}

###########################################
# CLOUDGUARD MANAGEMENT NETWORK INTERFACES
###########################################
resource "aws_network_interface" "management" {
  description       = "eth0"
  subnet_id         = var.subnet_id
  security_groups   = [aws_security_group.management.id]
  source_dest_check = true
}

#####################################
# CLOUDGUARD MANAGEMENT EC2 INSTANCE
#####################################
resource "aws_instance" "management" {
  ami                  = var.image_id
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.management.name
  key_name             = var.key_name
  network_interface {
    device_index         = "0"
    network_interface_id = aws_network_interface.management.id
  }
  ebs_block_device {
    device_name = "/dev/xvda"
    volume_type = "gp2"
    volume_size = "100"
  }
  lifecycle {
    ignore_changes = [
      ebs_block_device,
    ]
  }
  tags = {
    Name = var.management_name
  }
  user_data_base64 = base64encode(<<EOF
    #!/bin/bash
    echo
  EOF
  )
}

