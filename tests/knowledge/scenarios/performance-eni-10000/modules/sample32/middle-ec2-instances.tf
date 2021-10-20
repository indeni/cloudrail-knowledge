resource "aws_instance" "middle_subnet_0" {
  count                  = local.instances_middle_per_subnet
  ami                    = data.aws_ami.ami.id
  instance_type          = "t2.micro"
  subnet_id              = module.middle.private_subnets[0]
  vpc_security_group_ids = [aws_security_group.middle-sg.id]
  iam_instance_profile   = aws_iam_instance_profile.middle-instance-profile.id
}

resource "aws_network_interface" "eni_subnet_03" {
  count           = local.instances_middle_per_subnet
  subnet_id       = module.middle.private_subnets[3]
  security_groups = [aws_security_group.middle-sg-backoffice.id]
}

resource "aws_network_interface_attachment" "eni_subnet_03" {
  count                = local.instances_middle_per_subnet
  instance_id          = aws_instance.middle_subnet_0[count.index].id
  network_interface_id = aws_network_interface.eni_subnet_03[count.index].id
  device_index         = 1
}


resource "aws_instance" "middle_subnet_1" {
  count                  = local.instances_middle_per_subnet
  ami                    = data.aws_ami.ami.id
  instance_type          = "t2.micro"
  subnet_id              = module.middle.private_subnets[1]
  vpc_security_group_ids = [aws_security_group.middle-sg.id]
  iam_instance_profile   = aws_iam_instance_profile.middle-instance-profile.id
}

resource "aws_network_interface" "eni_subnet_14" {
  count           = local.instances_middle_per_subnet
  subnet_id       = module.middle.private_subnets[4]
  security_groups = [aws_security_group.middle-sg-backoffice.id]
}

resource "aws_network_interface_attachment" "eni_subnet_14" {
  count                = local.instances_middle_per_subnet
  instance_id          = aws_instance.middle_subnet_1[count.index].id
  network_interface_id = aws_network_interface.eni_subnet_14[count.index].id
  device_index         = 1
}


resource "aws_instance" "middle_subnet_2" {
  count                  = local.instances_middle_per_subnet
  ami                    = data.aws_ami.ami.id
  instance_type          = "t2.micro"
  subnet_id              = module.middle.private_subnets[5]
  vpc_security_group_ids = [aws_security_group.middle-sg.id]
  iam_instance_profile   = aws_iam_instance_profile.middle-instance-profile.id
}

resource "aws_network_interface" "eni_subnet_25" {
  count           = local.instances_middle_per_subnet
  subnet_id       = module.middle.private_subnets[5]
  security_groups = [aws_security_group.middle-sg-backoffice.id]
}

resource "aws_network_interface_attachment" "eni_subnet_25" {
  count                = local.instances_middle_per_subnet
  instance_id          = aws_instance.middle_subnet_2[count.index].id
  network_interface_id = aws_network_interface.eni_subnet_25[count.index].id
  device_index         = 1
}

# Security group allow access from MGMT
resource "aws_security_group" "middle-sg" {
  name        = "middle-sg"
  description = "Security group for MIDDLEWARE instances"
  vpc_id      = module.middle.vpc_id
}

resource "aws_security_group_rule" "middle-ingress-rule1" {
  type                     = "ingress"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.mgmt-sg.id

  security_group_id = aws_security_group.middle-sg.id
}

resource "aws_security_group_rule" "middle-egress-rule1" {
  type                     = "egress"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.mgmt-sg.id

  security_group_id = aws_security_group.middle-sg.id
}


# Security group allow access to/from BACKOFFICE
resource "aws_security_group" "middle-sg-backoffice" {
  name        = "middle-to-backoffice-sg"
  description = "Security group for MIDDLEWARE instances to Backoffice"
  vpc_id      = module.middle.vpc_id
}

resource "aws_security_group_rule" "middle-back-ingress-rule1" {
  type        = "ingress"
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.middle-sg-backoffice.id
}

resource "aws_security_group_rule" "middle-back-egress-rule1" {
  type        = "egress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.middle-sg-backoffice.id
}

resource "aws_iam_instance_profile" "middle-instance-profile" {
  name = "middle-instance-profile"
  role = aws_iam_role.middle-instance.name
}

resource "aws_iam_role" "middle-instance" {
  name = "middle-instance"
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
