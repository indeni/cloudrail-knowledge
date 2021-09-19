locals {
  http_port = 80
  max_port = 65535
  cidr_block = "192.168.100.128/25"
  zero_cidr_block = "0.0.0.0/0"
}



resource "aws_vpc" "test-vpc" {
  cidr_block           = local.cidr_block
}

resource "aws_subnet" "public-subnet" {
  vpc_id     = aws_vpc.test-vpc.id
  cidr_block = local.cidr_block
  availability_zone = "us-east-1a"
}

resource "aws_network_acl" "public-subnet-nacl" {
  vpc_id     = aws_vpc.test-vpc.id
  subnet_ids = [aws_subnet.public-subnet.id]
}

resource "aws_network_acl_rule" "inbound-rule" {
  network_acl_id = aws_network_acl.public-subnet-nacl.id
  rule_number    = 100
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = local.zero_cidr_block
  from_port      = local.http_port
  to_port        = local.http_port
}

resource "aws_network_acl_rule" "outbound-rule" {
  network_acl_id = aws_network_acl.public-subnet-nacl.id
  rule_number    = 100
  egress         = true
  protocol       = -1
  rule_action    = "allow"
  cidr_block     = local.zero_cidr_block
  from_port      = 0
  to_port        = 0
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.test-vpc.id
}

resource "aws_route_table" "public-subnet-rt" {
  vpc_id = aws_vpc.test-vpc.id
}

resource "aws_route" "igw-route" {
  route_table_id         = aws_route_table.public-subnet-rt.id
  destination_cidr_block = local.zero_cidr_block
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route_table_association" "public-subnet-rt-assoc" {
  subnet_id      = aws_subnet.public-subnet.id
  route_table_id = aws_route_table.public-subnet-rt.id
}


resource "aws_security_group" "target-ecs-sg" {
  name   = "target-ecs-sg"
  vpc_id = aws_vpc.test-vpc.id

  ingress {
    description = "target-ecs-sg"
    from_port   = local.http_port
    to_port     = local.http_port
    protocol    = "tcp"
    cidr_blocks = [local.zero_cidr_block]
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
      "image": "167389268608.dkr.ecr.us-east-1.amazonaws.com/apache-web-server:latest",
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
  network_mode = "awsvpc"
  memory = "512"
  cpu = "256"
  requires_compatibilities = ["FARGATE"]
}

data "aws_ecs_container_definition" "container-definition" {
  task_definition = aws_ecs_task_definition.web-server-task-definition.id
  container_name  = "apache-web-server"
}

resource "aws_cloudwatch_event_target" "web-server-et" {
  target_id = "web-server-target-id"
  rule      = aws_cloudwatch_event_rule.web-server-schedule-every-1d-rule.name
  arn       = aws_ecs_cluster.ecs-cluster.arn

  ecs_target {
    task_count = 1
    task_definition_arn = aws_ecs_task_definition.web-server-task-definition.arn
    launch_type = "FARGATE"
    network_configuration {
      subnets = [aws_subnet.public-subnet.id]
      security_groups = [aws_security_group.target-ecs-sg.id]
      assign_public_ip = true
    }
  }

  role_arn = data.aws_iam_role.ecs_task_execution_role.arn
}

resource "aws_cloudwatch_event_rule" "web-server-schedule-every-1d-rule" {
  name        = "web-server-schedule-every-1d-rule"
  schedule_expression = "rate(24 hours)"
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "AWSServiceRoleForECS"
}