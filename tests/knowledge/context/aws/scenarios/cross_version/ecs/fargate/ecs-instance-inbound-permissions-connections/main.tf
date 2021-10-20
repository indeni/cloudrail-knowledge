locals {
  region  = "us-east-1"
  http_port = 80
  max_port = 65535
  cidr_block = "192.168.100.128/25"
  zero_cidr_block = "0.0.0.0/0"
  s3_prefix_list_cidr_block = "54.231.0.0/17"
}



resource "aws_vpc" "test-vpc" {
  cidr_block           = local.cidr_block
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.test-vpc.id
  cidr_block = local.cidr_block
  availability_zone = "us-east-1a"
}

resource "aws_security_group" "http-sg" {
  name   = "sg"
  vpc_id = aws_vpc.test-vpc.id

  ingress {
    description = "mysql"
    from_port   = local.http_port
    to_port     = local.http_port
    protocol    = "tcp"
    cidr_blocks = [local.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [local.zero_cidr_block]
  }

}

resource "aws_ecs_cluster" "ecs-cluster" {
  name = "ecs-cluster"
}

resource "aws_ecs_task_definition" "web-server-task-definition" {
  family                = "web-server-task"
  container_definitions = <<DEFINITION
  [
    {
      "name": "apache-web-server",
      "image": "/ecr/repository/image/path",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        }
      ]
    }
  ]
  DEFINITION
  execution_role_arn = data.aws_iam_role.ecs_task_execution_role.arn
  task_role_arn = aws_iam_role.ecs-instance-role.arn
  network_mode = "awsvpc"
  memory = "512"
  cpu = "256"
  requires_compatibilities = ["FARGATE"]
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "AWSServiceRoleForECS"
}

resource "aws_iam_role" "ecs-instance-role" {
  name = "ecs-instance-role-test"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ecs.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

}

resource "aws_ecs_service" "web-server-service" {
  name            = "web-server-service"
  cluster         = aws_ecs_cluster.ecs-cluster.id
  task_definition = aws_ecs_task_definition.web-server-task-definition.arn
  desired_count   = 1
  launch_type = "FARGATE"

  network_configuration {
    subnets = [aws_subnet.private-subnet.id]
    security_groups = [aws_security_group.http-sg.id]
    assign_public_ip = false
  }
}

resource "aws_iam_user" "user-1" {
  name = "user-1"
}

resource "aws_iam_user_policy" "user-1-policy" {
  name = "user-1-policy"
  user = aws_iam_user.user-1.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ecs:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}