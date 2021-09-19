locals {
  region  = "us-east-2"
  mysql_port = 3306
  web_server_port = 80
}


resource "aws_vpc" "test-vpc" {
  cidr_block           = "192.168.10.0/24"
}

resource "aws_subnet" "public-subnet" {
  vpc_id     = aws_vpc.test-vpc.id
  cidr_block = "192.168.10.0/24"
  availability_zone = format("%sa", local.region)
}

resource "aws_network_acl" "public-nacl" {
  vpc_id     = aws_vpc.test-vpc.id
  subnet_ids = [aws_subnet.public-subnet.id]
}

resource "aws_network_acl_rule" "inbound-rule" {
  network_acl_id = aws_network_acl.public-nacl.id
  rule_number    = 100
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = local.web_server_port
  to_port        = local.mysql_port
}

resource "aws_network_acl_rule" "outbound-rule" {
  network_acl_id = aws_network_acl.public-nacl.id
  rule_number    = 100
  egress         = true
  protocol       = -1
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
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
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route_table_association" "public-subnet-rt-assoc" {
  subnet_id      = aws_subnet.public-subnet.id
  route_table_id = aws_route_table.public-subnet-rt.id
}


resource "aws_security_group" "sg" {
  name   = "sg"
  vpc_id = aws_vpc.test-vpc.id

  ingress {
    description = "mysql"
    from_port   = local.web_server_port
    to_port     = local.mysql_port
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


resource "aws_launch_template" "foobar" {
  name_prefix   = "foobar"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}

resource "aws_autoscaling_group" "test" {
  name = "asg for ecs"
  availability_zones = [format("%sa", local.region)]
  desired_capacity = 1
  max_size = 5
  min_size = 1

  launch_template {
    id      = aws_launch_template.foobar.id
    version = "$Latest"
  }

  tag {
    key                 = "AmazonECSManaged"
    value               = ""
    propagate_at_launch = true
  }

}

resource "aws_ecs_capacity_provider" "test" {
  name = "test"

  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.test.arn

    managed_scaling {
      maximum_scaling_step_size = 1000
      minimum_scaling_step_size = 1
      status                    = "ENABLED"
      target_capacity           = 10
    }
  }
}

resource "aws_ecs_cluster" "ecs-cluster" {
  name = "ecs-cluster"
  capacity_providers = [aws_ecs_capacity_provider.test.name]
}

data "aws_ecs_container_definition" "web-server-container" {
  task_definition = aws_ecs_task_definition.web-server-task-definition.id
  container_name  = "apache-web-server"
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
  execution_role_arn = "arn:aws:iam::111111111111:role/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS"
  network_mode = "awsvpc"
  memory = "256"
  cpu = "256"
  requires_compatibilities = ["EC2"]
}

data "aws_ecs_container_definition" "container-definition" {
  task_definition = aws_ecs_task_definition.web-server-task-definition.id
  container_name  = "apache-web-server"
}

resource "aws_lb" "public-elb" {
  name               = "public-elb"
  internal           = false
  load_balancer_type = "network"
  subnets            = [aws_subnet.public-subnet.id]

}

resource "aws_ecs_service" "web-server-service" {
  name = "web-server-service"
  cluster         = aws_ecs_cluster.ecs-cluster.arn
  task_definition = aws_ecs_task_definition.web-server-task-definition.arn
  desired_count   = 1
  launch_type = "EC2"

  network_configuration {
    subnets = [aws_subnet.public-subnet.id]
    security_groups = [aws_security_group.sg.id]
  }

    load_balancer {
    target_group_arn = aws_lb_target_group.elb-tg.arn
    container_name   = data.aws_ecs_container_definition.web-server-container.container_name
    container_port   = 80
  }
}

resource "aws_lb_target_group" "elb-tg" {

  name     = "elb-tg"
  port     = 80
  protocol = "TCP"
  vpc_id   = aws_vpc.test-vpc.id
  target_type = "ip"

  health_check {
    interval = 10
    port     = 80
    protocol = "TCP"
  }

}

resource "aws_lb_listener" "test" {
  load_balancer_arn = aws_lb.public-elb.id
  port = 80
  protocol = "TCP"

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.elb-tg.id
  }
}

//resource "aws_iam_service_linked_role" "ecs" {
//  aws_service_name = "ecs.amazonaws.com"
//}