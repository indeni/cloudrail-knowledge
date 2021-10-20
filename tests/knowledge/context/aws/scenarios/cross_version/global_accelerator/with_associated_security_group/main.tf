
resource "aws_vpc" "nondefault" {
  cidr_block = "10.1.1.0/24"
}

resource "aws_subnet" "nondefault_1" {
  vpc_id = aws_vpc.nondefault.id
  cidr_block = "10.1.1.128/25"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "nondefault_2" {
  vpc_id = aws_vpc.nondefault.id
  cidr_block = "10.1.1.0/25"
  availability_zone = "us-east-1b"
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.nondefault.id

  tags = {
    Name = "main"
  }
}

resource "aws_route_table" "public-rtb" {
  vpc_id = aws_vpc.nondefault.id

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


resource "aws_globalaccelerator_accelerator" "test" {
  name            = "ga-test"
  ip_address_type = "IPV4"
}

resource "aws_globalaccelerator_endpoint_group" "test" {
  listener_arn = aws_globalaccelerator_listener.test.id

  endpoint_configuration {
    endpoint_id                    = aws_lb.test.arn
    client_ip_preservation_enabled = true
  }
}

resource "aws_globalaccelerator_listener" "test" {
  accelerator_arn = aws_globalaccelerator_accelerator.test.id
  client_affinity = "SOURCE_IP"
  protocol        = "TCP"

  port_range {
    from_port = 80
    to_port   = 80
  }
}

resource "aws_lb" "test" {
  name                       = "test-lb-tf"
  internal                   = true
  load_balancer_type         = "application"
  subnets                    = [aws_subnet.nondefault_2.id, aws_subnet.nondefault_1.id]
  enable_deletion_protection = false
}
