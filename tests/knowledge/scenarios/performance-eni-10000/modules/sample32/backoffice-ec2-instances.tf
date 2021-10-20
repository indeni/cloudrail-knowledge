resource "aws_instance" "back_subnet_0" {
  count                  = local.instances_back_per_subnet
  ami                    = data.aws_ami.ami.id
  instance_type          = "t2.micro"
  subnet_id              = module.back.private_subnets[0]
  vpc_security_group_ids = [aws_security_group.back-sg.id]
  iam_instance_profile   = aws_iam_instance_profile.back-instance-profile.id
}

resource "aws_network_interface" "back_eni_subnet_03" {
  count           = local.instances_back_per_subnet
  subnet_id       = module.back.private_subnets[3]
  security_groups = [aws_security_group.backoffice-sg-middleware.id]
}

resource "aws_network_interface_attachment" "back_eni_subnet_03" {
  count                = local.instances_back_per_subnet
  instance_id          = aws_instance.back_subnet_0[count.index].id
  network_interface_id = aws_network_interface.back_eni_subnet_03[count.index].id
  device_index         = 1
}

resource "aws_instance" "back_subnet_1" {
  count                  = local.instances_back_per_subnet
  ami                    = data.aws_ami.ami.id
  instance_type          = "t2.micro"
  subnet_id              = module.back.private_subnets[1]
  vpc_security_group_ids = [aws_security_group.back-sg.id]
  iam_instance_profile   = aws_iam_instance_profile.back-instance-profile.id
}

resource "aws_network_interface" "back_eni_subnet_14" {
  count           = local.instances_back_per_subnet
  subnet_id       = module.back.private_subnets[4]
  security_groups = [aws_security_group.backoffice-sg-middleware.id]
}

resource "aws_network_interface_attachment" "back_eni_subnet_14" {
  count                = local.instances_back_per_subnet
  instance_id          = aws_instance.back_subnet_1[count.index].id
  network_interface_id = aws_network_interface.back_eni_subnet_14[count.index].id
  device_index         = 1
}

resource "aws_instance" "back_subnet_2" {
  count                  = local.instances_back_per_subnet
  ami                    = data.aws_ami.ami.id
  instance_type          = "t2.micro"
  subnet_id              = module.back.private_subnets[5]
  vpc_security_group_ids = [aws_security_group.back-sg.id]
  iam_instance_profile   = aws_iam_instance_profile.back-instance-profile.id
}

resource "aws_network_interface" "back_eni_subnet_25" {
  count           = local.instances_back_per_subnet
  subnet_id       = module.back.private_subnets[5]
  security_groups = [aws_security_group.backoffice-sg-middleware.id]
}

resource "aws_network_interface_attachment" "back_eni_subnet_25" {
  count                = local.instances_back_per_subnet
  instance_id          = aws_instance.back_subnet_2[count.index].id
  network_interface_id = aws_network_interface.back_eni_subnet_25[count.index].id
  device_index         = 1
}

# Security group allow access from MGMT
resource "aws_security_group" "back-sg" {
  name        = "back-sg"
  description = "Security group for BACKOFFICE instances"
  vpc_id      = module.back.vpc_id
}

resource "aws_security_group_rule" "back-ingress-rule1" {
  type                     = "ingress"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.mgmt-sg.id

  security_group_id = aws_security_group.back-sg.id
}

resource "aws_security_group_rule" "back-egress-rule1" {
  type                     = "egress"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.mgmt-sg.id

  security_group_id = aws_security_group.back-sg.id
}

# Security group allow access to/from MIDDLEWARE
resource "aws_security_group" "backoffice-sg-middleware" {
  name        = "back-to-middle-sg"
  description = "Security group for BACKOFFICE instances to Middleware"
  vpc_id      = module.back.vpc_id
}

resource "aws_security_group_rule" "back-middle-ingress-rule1" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  source_security_group_id = aws_security_group.middle-sg-backoffice.id

  security_group_id = aws_security_group.backoffice-sg-middleware.id
}

resource "aws_security_group_rule" "back-middle-egress-rule1" {
  type        = "egress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.backoffice-sg-middleware.id
}

resource "aws_iam_instance_profile" "back-instance-profile" {
  name = "back-instance-profile"
  role = aws_iam_role.back-instance.name
}

resource "aws_iam_role" "back-instance" {
  name = "back-instance"
  path = "/"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}
