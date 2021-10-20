
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


resource "aws_security_group" "test" {
  name        = "glue_connection_sg"
  description = "Glue Connection test SG"
  vpc_id      = aws_vpc.nondefault.id

  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}


resource "aws_glue_connection" "test" {
  name = "test_glue_connection"

  connection_properties = {
    JDBC_CONNECTION_URL = "jdbc:mysql://justfakedatahere/exampledatabase"
    PASSWORD            = "examplepassword" # Bad practice. Just for testing purposes
    USERNAME            = "exampleusername"
  }


  physical_connection_requirements {
    availability_zone = aws_subnet.nondefault_1.availability_zone
    security_group_id_list = [aws_security_group.test.id]
    subnet_id              = aws_subnet.nondefault_1.id
  }
}
