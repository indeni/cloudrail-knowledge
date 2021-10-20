data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name = "name"

    values = [
      "amzn-ami-hvm-*-x86_64-gp2",
    ]
  }
}

resource "aws_autoscaling_group" "asg" {
  launch_configuration = aws_launch_configuration.as_conf.name
  min_size             = local.asg_instances
  max_size             = local.asg_instances
  health_check_type    = "ELB"
  vpc_zone_identifier  = module.vpcA.private_subnets
  target_group_arns    = [aws_lb_target_group.this.arn]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_instance_profile" "as_conf_instance" {
  name = "${local.nameA}-instance-profile"
  role = aws_iam_role.as_conf_role.name
}

resource "aws_iam_role" "as_conf_role" {
  name               = "${local.nameA}-instance-profile-role"
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

  inline_policy {
    name = "Cloudwatch"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["logs:PutLogEvents"]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }

  inline_policy {
    name = "SSM"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["ssm:DescribeParameters"]
          Effect   = "Allow"
          Resource = "*"
        },
        {
          Action   = ["ssm:GetParameters"]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }
}


resource "aws_launch_configuration" "as_conf" {
  image_id             = data.aws_ami.amazon_linux.id
  instance_type        = "t2.micro"
  security_groups      = [aws_security_group.asg_sg.id]
  iam_instance_profile = aws_iam_instance_profile.as_conf_instance.name

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "asg_sg" {
  description = "Security group for the ASG"
  vpc_id      = module.vpcA.vpc_id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.lb_sg.id]
  }
}
