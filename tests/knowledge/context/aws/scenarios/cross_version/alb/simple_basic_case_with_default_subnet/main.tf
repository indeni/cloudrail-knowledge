data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_default_vpc" "def" {

}

resource "aws_default_subnet" "def1" {
  availability_zone = data.aws_availability_zones.available.names[0]
}

resource "aws_default_subnet" "def2" {
  availability_zone = data.aws_availability_zones.available.names[1]
}

resource "aws_lb" "test" {
  name = "test123"
  load_balancer_type = "application"
  subnets = [aws_default_subnet.def1.id, aws_default_subnet.def2.id]

}