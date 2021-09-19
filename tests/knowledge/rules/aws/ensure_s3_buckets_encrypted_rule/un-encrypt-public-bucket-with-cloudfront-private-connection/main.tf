provider "aws" {
  region = "us-east-1"
}

locals {
  bucket_name  = "static-web-resources-bucket"
  s3_origin_id = "${local.bucket_name}-origin-id"
}

resource "aws_s3_bucket" "static-web-resources-bucket" {
  bucket = local.bucket_name
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "AllowCloudFrontOAI",
  "Statement": [
    {
      "Sid": "AllowCloudFrontOAI",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:GetObject",
      "Resource": ["arn:aws:s3:::${local.bucket_name}", "arn:aws:s3:::${local.bucket_name}/*"]
    }
  ]
}
POLICY
}

resource "aws_cloudfront_origin_access_identity" "cloudfront-oai-user" {
  comment = local.bucket_name
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  enabled             = true

  origin {
    domain_name = aws_s3_bucket.static-web-resources-bucket.bucket_regional_domain_name
    origin_id   = local.s3_origin_id
    origin_path = "/web-resources"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.cloudfront-oai-user.cloudfront_access_identity_path
    }
  }

  restrictions {
    geo_restriction {
      locations = ["IL", "US"]
      restriction_type = "whitelist"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
    minimum_protocol_version = "TLSv1"
    ssl_support_method = "sni-only"
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id          = local.s3_origin_id
    viewer_protocol_policy = "redirect-to-https"
    trusted_signers = ["self"]

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

}