data "aws_ami" "ecs_ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn-ami-*-amazon-ecs-optimized"]
  }
}

resource "aws_autoscaling_group" "asg" {
  launch_configuration = aws_launch_configuration.as_conf.name
  min_size             = local.ec2_instances
  max_size             = local.ec2_instances
  health_check_type    = "EC2"
  vpc_zone_identifier  = module.vpcB.private_subnets

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [null_resource.enable_new_ecs_features]
}


resource "aws_launch_configuration" "as_conf" {
  image_id             = data.aws_ami.ecs_ami.id
  instance_type        = local.instance_type
  security_groups      = [aws_security_group.asg_sg.id]
  iam_instance_profile = aws_iam_instance_profile.as_conf_instance.name
  user_data            = "#!/bin/bash\necho ECS_CLUSTER=${local.name}-ECSCluster >> /etc/ecs/ecs.config"

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [aws_ecs_cluster.ecs_cluster]
}

resource "aws_iam_instance_profile" "as_conf_instance" {
  name = "${local.name}-instance-profile"
  role = aws_iam_role.as_conf_role.name
}

resource "aws_iam_role" "as_conf_role" {
  name               = "${local.name}-instance-profile-role"
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

resource "aws_iam_role_policy_attachment" "role_attachment" {
  role       = aws_iam_role.as_conf_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_security_group" "asg_sg" {
  description = "Security group for the ASG"
  vpc_id      = module.vpcB.vpc_id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port       = 80
    to_port         = 83
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs-lb-sg.id]
  }
}
