provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.1.1.0/24"
  enable_dns_hostnames = true

}

resource "aws_subnet" "nondefault_1" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.1.1.128/25"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "nondefault_2" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.1.1.0/25"
  availability_zone = "us-east-1b"
}

resource "aws_security_group" "allow_access" {
  name        = "Allow access Security Group"
  description = "Allow all traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main"
  }
}

resource "aws_route_table" "public-rtb" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "public-rtb"
  }
}

resource "aws_route_table_association" "public-rtb-assoc_1" {
  route_table_id = aws_route_table.public-rtb.id
  subnet_id = aws_subnet.nondefault_1.id
}

resource "aws_route_table_association" "public-rtb-assoc_2" {
  route_table_id = aws_route_table.public-rtb.id
  subnet_id = aws_subnet.nondefault_2.id
}


resource "aws_lb" "alb_test" {
  subnets = [aws_subnet.nondefault_1.id, aws_subnet.nondefault_2.id]
  load_balancer_type = "application"
}

resource "aws_lb_listener" "mrw-lb-listener" {
  load_balancer_arn = aws_lb.alb_test.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
    type = "redirect"
  }
}

resource "aws_apigatewayv2_api" "mrw-api" {
  name          = "mrw-http-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_vpc_link" "mrw-link" {
  name               = "mrw-link"
  security_group_ids = [aws_security_group.allow_access.id]
  subnet_ids         = [aws_subnet.nondefault_1.id, aws_subnet.nondefault_2.id]

}

resource "aws_apigatewayv2_route" "healthcheck" {
  api_id    = aws_apigatewayv2_api.mrw-api.id
  route_key = "GET /"
  target    = "integrations/${aws_apigatewayv2_integration.mrw-int-get.id}"
}

resource "aws_apigatewayv2_integration" "mrw-int-get" {
  api_id             = aws_apigatewayv2_api.mrw-api.id
  integration_type   = "HTTP_PROXY"
  connection_type    = "VPC_LINK"
  connection_id      = aws_apigatewayv2_vpc_link.mrw-link.id
  integration_uri    = aws_lb_listener.mrw-lb-listener.arn
  integration_method = "GET"

}

resource "aws_security_group" "unused" {
  vpc_id     = aws_vpc.main.id
  name = "Unused security group"

  ingress {
    from_port = 53
    protocol = "UDP"
    to_port = 53
    cidr_blocks = ["0.0.0.0/0"]
  }
}