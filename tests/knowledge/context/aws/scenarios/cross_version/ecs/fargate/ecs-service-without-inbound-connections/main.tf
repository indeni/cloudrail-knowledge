locals {
  region  = "us-east-1"
  http_port = 80
  max_port = 65535
  cidr_block = "192.168.100.128/25"
  zero_cidr_block = "0.0.0.0/0"
}

resource "aws_vpc" "test-vpc" {
  cidr_block           = local.cidr_block
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.test-vpc.id
}

resource "aws_default_route_table" "default_route_table" {
  default_route_table_id = aws_vpc.test-vpc.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "default table"
  }
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
          "containerPort": 8080,
          "hostPort": 8080,
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
  name = "ecs-instance-role"

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


resource "aws_instance" "web-server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id = aws_subnet.private-subnet.id
  vpc_security_group_ids = [aws_security_group.http-sg.id]
  tags = {
    Name = "HelloWorld"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}
