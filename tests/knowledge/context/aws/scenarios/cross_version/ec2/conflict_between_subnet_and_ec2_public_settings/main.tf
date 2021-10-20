resource "aws_vpc" "VPC" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "my-vpc"
  }
}

resource "aws_subnet" "PublicSubnet1" {
  cidr_block = "10.0.0.0/24"
  map_public_ip_on_launch = true
  vpc_id = aws_vpc.VPC.id

  tags = {
    Name = "Public Subnet AZ A"
  }
}

resource "aws_route_table" "RouteTablePublic" {
  vpc_id = aws_vpc.VPC.id
  depends_on = [ aws_internet_gateway.Igw ]

  tags = {
    Name = "Public Route Table"
  }

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.Igw.id
  }
}

resource "aws_route_table_association" "AssociationForRouteTablePublic0" {
  subnet_id = aws_subnet.PublicSubnet1.id
  route_table_id = aws_route_table.RouteTablePublic.id
}

resource "aws_internet_gateway" "Igw" {
  vpc_id = aws_vpc.VPC.id
}

### EC2 Linux

resource "aws_security_group" "LinuxSG" {
  name = "Linux-sg"
  description = "Linux EC2 security group."
  vpc_id = aws_vpc.VPC.id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "ubunbtu" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  security_groups = [aws_security_group.LinuxSG.id]
  subnet_id = aws_subnet.PublicSubnet1.id
  associate_public_ip_address = "false"

  tags = {
    Name = "Linux Instance"
  }
}
