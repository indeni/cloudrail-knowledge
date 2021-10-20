resource "aws_instance" "mgmt_subnet_0" {
  count                  = local.instances_mgmt_per_subnet
  ami                    = data.aws_ami.ami.id
  instance_type          = "t2.micro"
  subnet_id              = module.mgmt.private_subnets[0]
  vpc_security_group_ids = [aws_security_group.mgmt-sg.id]
  iam_instance_profile   = aws_iam_instance_profile.mgmt-instance-profile.id
}

resource "aws_instance" "mgmt_subnet_1" {
  count                  = local.instances_mgmt_per_subnet
  ami                    = data.aws_ami.ami.id
  instance_type          = "t2.micro"
  subnet_id              = module.mgmt.private_subnets[1]
  vpc_security_group_ids = [aws_security_group.mgmt-sg.id]
  iam_instance_profile   = aws_iam_instance_profile.mgmt-instance-profile.id
}


resource "aws_security_group" "mgmt-sg" {
  name        = "mgmt-sg"
  description = "Security group for MGMT instances"
  vpc_id      = module.mgmt.vpc_id
}

resource "aws_security_group_rule" "mgmt-ingress-rule1" {
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.mgmt-sg.id
}

resource "aws_security_group_rule" "mgmt-egress-rule1" {
  type        = "egress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.mgmt-sg.id
}


resource "aws_iam_instance_profile" "mgmt-instance-profile" {
  name = "mgmt-instance-profile"
  role = aws_iam_role.mgmt-instance.name
}

resource "aws_iam_role" "mgmt-instance" {
  name = "mgmt-instance"
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
