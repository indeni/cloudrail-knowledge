resource "aws_vpc" "external" {
  cidr_block = "172.27.0.0/16"
  tags = {
    Name = "none-default-vpc"
  }
}
