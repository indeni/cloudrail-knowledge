################################################################################
# LOAD BALANCER
################################################################################
resource "aws_lb" "ecs_lb" {
  name                       = "${local.name}-ecs-lb"
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.ecs-lb-sg.id]
  subnets                    = module.vpcB.public_subnets
  enable_deletion_protection = false
}

resource "aws_security_group" "ecs-lb-sg" {
  name   = "${local.name}-ecs-fargate-sg-alb"
  vpc_id = module.vpcB.vpc_id

  ingress {
    protocol         = "tcp"
    from_port        = 80
    to_port          = 83
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_alb_target_group" "ecs_lb_tg_1" {
  name        = "${local.name}-ecs-lb-tg-1"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = module.vpcB.vpc_id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    port                = 80
    matcher             = "200"
    timeout             = "3"
    path                = "/"
    unhealthy_threshold = "2"
  }
}

resource "aws_alb_target_group" "ecs_lb_tg_2" {
  name        = "${local.name}-ecs-lb-tg-2"
  port        = 81
  protocol    = "HTTP"
  vpc_id      = module.vpcB.vpc_id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    port                = 81
    matcher             = "200"
    timeout             = "3"
    path                = "/"
    unhealthy_threshold = "2"
  }
}

resource "aws_alb_target_group" "ecs_lb_tg_3" {
  name        = "${local.name}-ecs-lb-tg-3"
  port        = 82
  protocol    = "HTTP"
  vpc_id      = module.vpcB.vpc_id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    port                = 82
    matcher             = "200"
    timeout             = "3"
    path                = "/"
    unhealthy_threshold = "2"
  }
}

resource "aws_alb_target_group" "ecs_lb_tg_4" {
  name        = "${local.name}-ecs-lb-tg-4"
  port        = 83
  protocol    = "HTTP"
  vpc_id      = module.vpcB.vpc_id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    port                = 83
    matcher             = "200"
    timeout             = "3"
    path                = "/"
    unhealthy_threshold = "2"
  }
}

resource "aws_alb_listener" "http_service_1" {
  load_balancer_arn = aws_lb.ecs_lb.id
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.ecs_lb_tg_1.arn
  }
}

resource "aws_alb_listener" "http_service_2" {
  load_balancer_arn = aws_lb.ecs_lb.id
  port              = 81
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.ecs_lb_tg_2.arn
  }
}

resource "aws_alb_listener" "http_service_3" {
  load_balancer_arn = aws_lb.ecs_lb.id
  port              = 82
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.ecs_lb_tg_3.arn
  }
}

resource "aws_alb_listener" "http_service_4" {
  load_balancer_arn = aws_lb.ecs_lb.id
  port              = 83
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.ecs_lb_tg_4.arn
  }
}
