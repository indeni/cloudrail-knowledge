
data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "test" {
  bucket        = "test-trail-multiregion-enabled-kajhdsf78yf"
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
            "Resource": "arn:aws:s3:::test-trail-multiregion-enabled-kajhdsf78yf"
        },
        {
            "Sid": "AWSCloudTrailWrite",
            "Effect": "Allow",
            "Principal": {
              "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::test-trail-multiregion-enabled-kajhdsf78yf/prefix/AWSLogs/${data.aws_caller_identity.current.account_id}/*",
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

resource "aws_cloudtrail" "test" {
  name                  = "test-trail-multiregion-enabled"
  s3_bucket_name        = aws_s3_bucket.test.id
  s3_key_prefix         = "prefix"
  is_multi_region_trail = true
}
