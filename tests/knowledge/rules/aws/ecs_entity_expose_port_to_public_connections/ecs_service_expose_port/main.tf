locals {
  region  = "us-east-1"
  ssh_port = 22
}

provider "aws" {
  region  = "us-east-1"
}

resource "aws_vpc" "main-vpc" {
  cidr_block           = "192.168.10.0/24"
}

resource "aws_subnet" "main-public-subnet" {
  vpc_id     = aws_vpc.main-vpc.id
  cidr_block = "192.168.10.0/24"
  availability_zone = local.region
}

resource "aws_network_acl" "public-subnet-nacl" {
  vpc_id     = aws_vpc.main-vpc.id
  subnet_ids = [aws_subnet.main-public-subnet.id]
}

resource "aws_network_acl_rule" "inbound-rule" {
  network_acl_id = aws_network_acl.public-subnet-nacl.id
  rule_number    = 100
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = local.ssh_port
  to_port        = local.ssh_port
}

resource "aws_network_acl_rule" "outbound-rule" {
  network_acl_id = aws_network_acl.public-subnet-nacl.id
  rule_number    = 100
  egress         = true
  protocol       = -1
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 0
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main-vpc.id
}

resource "aws_route_table" "public-subnet-rt" {
  vpc_id = aws_vpc.main-vpc.id
}

resource "aws_route" "igw-route" {
  route_table_id         = aws_route_table.public-subnet-rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route_table_association" "public-subnet-rt-assoc" {
  subnet_id      = aws_subnet.main-public-subnet.id
  route_table_id = aws_route_table.public-subnet-rt.id
}


resource "aws_security_group" "sg" {
  name   = "sg"
  vpc_id = aws_vpc.main-vpc.id

  ingress {
    description = "mysql"
    from_port   = local.ssh_port
    to_port     = local.ssh_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
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
          "containerPort": 22,
          "hostPort": 22,
          "protocol": "tcp"
        }
      ]
    }
  ]
  DEFINITION
  execution_role_arn = "arn:aws:iam::167389268608:role/ecsExecRole"
  network_mode = "awsvpc"
  memory = "512"
  cpu = "256"
  requires_compatibilities = ["FARGATE"]
}

data "aws_ecs_container_definition" "container-definition" {
  task_definition = aws_ecs_task_definition.web-server-task-definition.id
  container_name  = "web-server"
}

resource "aws_ecs_service" "web-server-service" {
  name = "web-server-service"
  cluster         = aws_ecs_cluster.ecs-cluster.arn
  task_definition = aws_ecs_task_definition.web-server-task-definition.arn
  desired_count   = 1
  launch_type = "FARGATE"

  network_configuration {
    subnets = [aws_subnet.main-public-subnet.id]
    security_groups = [aws_security_group.sg.id]
    assign_public_ip = true
  }
}