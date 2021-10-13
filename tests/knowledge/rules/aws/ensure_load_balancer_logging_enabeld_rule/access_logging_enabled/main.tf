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

data "aws_elb_service_account" "main" {}

data "aws_iam_policy_document" "logging" {
  version = "2012-10-17"
  statement {
    sid    = "Enable ELB logging"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [data.aws_elb_service_account.main.arn]
    }
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.logging.arn}/elb/*"]
  }
}

resource "aws_s3_bucket_policy" "logging" {
  bucket = aws_s3_bucket.logging.id
  policy = data.aws_iam_policy_document.logging.json
}


resource "aws_s3_bucket" "logging" {
  acl           = "private"
  force_destroy = true
}

resource "aws_lb" "test" {
  name               = "lb-test-logging"
  internal           = true
  load_balancer_type = "application"
  subnets            = tolist(data.aws_subnet_ids.default.ids)

  access_logs {
    bucket  = aws_s3_bucket.logging.bucket
    prefix  = "elb"
    enabled = true
  }
}
