variable "environment" {
  type        = string
  description = "Name of the environment"
  default     = "development"
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources in"
  default     = "us-east-1"
}

variable "cidr_public" {
  type        = string
  description = "CIDR for public subnet"
  default     = "10.0.1.0/24"
}

variable "cidr_private" {
  type        = string
  description = "CIDR for private subnet"
  default     = "10.0.2.0/24"
}

resource "aws_vpc" "main" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name        = var.environment
    Environment = var.environment
  }
}

resource "aws_default_security_group" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = var.environment
    Environment = var.environment
  }
}


resource "aws_internet_gateway" "public" {
  // Allow instances within the public subnet
  // to have internet access
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "${var.environment}-internet-gateway"
    Environment = var.environment
  }
}

resource "aws_nat_gateway" "private" {
  // Allows instances in the private subnet
  // to establish outbound connections to the internet
  subnet_id            = aws_subnet.private.id
  allocation_id        = aws_eip.nat_gateway.id
  connectivity_type    = "public"
  depends_on = [
    aws_internet_gateway.public,
  ]
  tags = {
    Name        = "${var.environment}-nat-gateway-private"
    Environment = var.environment
  }
}

resource "aws_eip" "nat_gateway" {
  vpc = true
  tags = {
    Name        = "${var.environment}-private-nat-gateway-elastic-ip"
    Environment = var.environment
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name        = "${var.environment}-route-table-public"
    Environment = var.environment
    Public      = true
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name        = "${var.environment}-route-table-private"
    Environment = var.environment
    Public      = false
  }
}


resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route" "public_internet_route" {
  // Provide public subnet instances with
  // a route to the internet
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.public.id
  depends_on = [
    aws_route_table.public,
    aws_internet_gateway.public,
  ]
}

resource "aws_route" "private_internet_route" {
  // Provide private subnet instances with
  // a route to the internet
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.private.id
  depends_on = [
    aws_route_table.private,
    aws_nat_gateway.private,
  ]
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.cidr_public
  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.environment}-public"
    Environment = var.environment
    Public      = true
  }
}

resource "aws_subnet" "private" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.cidr_private
  map_public_ip_on_launch = false

  tags = {
    Name        = "${var.environment}-private"
    Environment = var.environment
    Public      = false
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

  owners = ["099720109477"]
}


resource "aws_network_interface" "default" {
  subnet_id = aws_subnet.public.id
  security_groups = [
    aws_security_group.default_ec2.id,
  ]

  tags = {
    Name        = "${var.environment}-default-network-interface"
    Environment = var.environment
  }
}

resource "aws_instance" "default" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.nano"

  network_interface {
    network_interface_id = aws_network_interface.default.id
    device_index         = 0
  }


  tags = {
    Name        = "${var.environment}-default"
    Environment = var.environment
  }
}

resource "aws_security_group" "default_ec2" {
  name        = "${var.environment}-default-ec2-security-group"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.environment}-default-ec2-security-group"
    Environment = var.environment
  }
}

resource "aws_security_group_rule" "default_ec2_ingress" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.default_ec2.id
}

resource "aws_security_group_rule" "default_ec2_egress" {
  type              = "egress"
from_port        = 0
to_port          = 0
protocol         = "-1"
cidr_blocks      = ["0.0.0.0/0"]
ipv6_cidr_blocks = ["::/0"]
  security_group_id = aws_security_group.default_ec2.id
}
