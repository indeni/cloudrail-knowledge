provider "aws" {
  region = "us-east-1"
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}

resource "aws_lb" "test" {
  name               = "lb-test-logging"
  internal           = true
  load_balancer_type = "application"
  subnets            = tolist(data.aws_subnet_ids.default.ids)
}
