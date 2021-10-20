data "aws_elb_service_account" "elb" {}

data "aws_iam_policy_document" "elb-logging" {
  version = "2012-10-17"
  statement {
    sid    = "Enable ELB logging"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [data.aws_elb_service_account.elb.arn]
    }
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.elb-logging.arn}/ELB-Logs/*"]
  }
}

resource "aws_s3_bucket" "elb-logging" {
  acl           = "private"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "elb-logging" {
  bucket                  = aws_s3_bucket.elb-logging.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "elb-logging" {
  bucket = aws_s3_bucket.elb-logging.id
  policy = data.aws_iam_policy_document.elb-logging.json
}

resource "aws_security_group" "lb_sg" {
  description = "Security group for the Load Balancer"
  vpc_id      = module.vpcA.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "this" {
  internal           = false
  load_balancer_type = "application"
  ip_address_type    = "ipv4"
  subnets            = module.vpcA.public_subnets
  security_groups    = [aws_security_group.lb_sg.id]

  access_logs {
    enabled = true
    bucket  = aws_s3_bucket.elb-logging.bucket
    prefix  = "ELB-Logs"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}

resource "aws_lb_target_group" "this" {
  port     = 80
  protocol = "HTTP"
  vpc_id   = module.vpcA.vpc_id

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 15
    timeout             = 3
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}
