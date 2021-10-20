resource "aws_lb" "test" {
  name                             = "${local.name}-nlb"
  internal                         = true
  load_balancer_type               = "network"
  subnets                          = module.vpc.public_subnets
  enable_cross_zone_load_balancing = true
}

resource "aws_lb_listener" "test" {
  load_balancer_arn = aws_lb.test.arn

  protocol = "TCP"
  port     = 80

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.test.arn
  }
}

resource "aws_lb_target_group" "test" {
  port     = 80
  protocol = "TCP"
  vpc_id   = module.vpc.vpc_id

  depends_on = [aws_lb.test]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_attachment" "test" {
  autoscaling_group_name = aws_autoscaling_group.asg.name
  alb_target_group_arn   = aws_lb_target_group.test.arn
}
