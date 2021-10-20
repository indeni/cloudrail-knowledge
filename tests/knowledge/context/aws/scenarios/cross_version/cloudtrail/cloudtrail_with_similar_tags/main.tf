
locals {
  name = "cloudtrail-logs-default-encryption"
}

data "aws_caller_identity" "current" {}

resource "aws_cloudtrail" "number_1" {
  name                          = local.name
  s3_bucket_name                = aws_s3_bucket.foo.id
  s3_key_prefix                 = "prefix"
  include_global_service_events = false
  tags = {
    Name = "Cloudtrail-test",
    Env = "Cloudtrail-testing-cloudtrail"
  }
}

resource "aws_cloudtrail" "number_2" {
  name                          = "${local.name}-2"
  s3_bucket_name                = aws_s3_bucket.foo.id
  s3_key_prefix                 = "prefix"
  include_global_service_events = false
  tags = {
    Name = "Cloudtrail-test-2",
    Env = "Cloudtrail-testing-cloudtrail-2"
  }
}

resource "aws_s3_bucket" "foo" {
  bucket        = local.name
  force_destroy = true

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck",
            "Effect": "Allow",
            "Principal": {
              "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::${local.name}"
        },
        {
            "Sid": "AWSCloudTrailWrite",
            "Effect": "Allow",
            "Principal": {
              "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::${local.name}/prefix/AWSLogs/${data.aws_caller_identity.current.account_id}/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}
POLICY
}