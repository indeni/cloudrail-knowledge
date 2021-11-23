resource "aws_security_group" "default_ec2" {
  name        = "${var.environment}-default-ec2-security-group"
  vpc_id      = data.aws_subnet.ec2_subnet.vpc_id

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
