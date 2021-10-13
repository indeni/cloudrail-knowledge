
data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}

resource "aws_lb" "test" {
  name                       = "test-lb-drop"
  internal                   = true
  load_balancer_type         = "application"
  subnets                    = data.aws_subnet_ids.default.ids
  drop_invalid_header_fields = true
}
