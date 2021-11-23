data "aws_subnet" "ec2_subnet" {
  id = var.ec2_subnet_id
}

resource "aws_network_interface" "default" {
  subnet_id = data.aws_subnet.ec2_subnet.id
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
