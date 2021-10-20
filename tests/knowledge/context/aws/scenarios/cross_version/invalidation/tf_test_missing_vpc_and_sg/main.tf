
resource "aws_subnet" "nondefault_1" {
  vpc_id = "vpc-1234567"
  cidr_block = "10.1.1.128/25"
  availability_zone = "us-east-1a"
}

resource "aws_launch_template" "test-launch-template" {
  name = "test-launch-template"
  image_id      = "ami-1a2b3c"
  instance_type = "t2.micro"

  network_interfaces {
    associate_public_ip_address = false
    security_groups = ["sg-1234567"]
    subnet_id = aws_subnet.nondefault_1.id
  }

}