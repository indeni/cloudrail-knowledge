provider "aws" {
  region = "us-west-1"
}

resource "aws_vpc" "vpc1" {
  cidr_block = "10.10.0.0/16"
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_subnet" "subnet1" {
  vpc_id = aws_vpc.vpc1.id
  cidr_block = "10.10.10.0/24"
  availability_zone_id = data.aws_availability_zones.available.zone_ids[0]
  tags = {
    Name = "subnet1"
  }
}

resource "aws_subnet" "subnet2" {
  vpc_id = aws_vpc.vpc1.id
  cidr_block = "10.10.11.0/24"
  availability_zone_id = data.aws_availability_zones.available.zone_ids[1]

  tags = {
    Name = "subnet2"
  }
}

resource "aws_internet_gateway" "igw1" {
  vpc_id = aws_vpc.vpc1.id
}

resource "aws_route_table" "rt1" {
  vpc_id = aws_vpc.vpc1.id
  route {
    gateway_id = aws_internet_gateway.igw1.id
    cidr_block = "0.0.0.0/0"
  }
}

resource "aws_route_table_association" "assoc1" {
  subnet_id = aws_subnet.subnet1.id
  route_table_id = aws_route_table.rt1.id
}

resource "aws_route_table_association" "assoc2" {
  subnet_id = aws_subnet.subnet2.id
  route_table_id = aws_route_table.rt1.id
}

resource "aws_lb_target_group" "test" {
  vpc_id = aws_vpc.vpc1.id
  port = 443
  protocol = "HTTPS"
}

resource "aws_lb" "alb_test" {
  subnets = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]
  load_balancer_type = "application"
}

resource "aws_lb_listener" "lb_listener_test" {
  load_balancer_arn = aws_lb.alb_test.arn
  port              = "443"
  protocol          = "HTTPS"
  certificate_arn = aws_acm_certificate.cert_test.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.test.arn
  }
}

resource "tls_private_key" "example" {
  algorithm = "RSA"
}

resource "tls_self_signed_cert" "example" {
  key_algorithm   = "RSA"
  private_key_pem = tls_private_key.example.private_key_pem

  subject {
    common_name  = "indeni.com"
    organization = "Indeni, Inc"
  }

  validity_period_hours = 12

  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "server_auth",
  ]
}

resource "aws_acm_certificate" "cert_test" {
  private_key      = tls_private_key.example.private_key_pem
  certificate_body = tls_self_signed_cert.example.cert_pem
}
