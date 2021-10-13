provider "aws" {
  region = "us-east-1"
}

variable "base_dir" {
  description = "Base dir"
  type = string
  default = "."
}

locals {
  bucket_id = "38456734875-blah"
}
resource "aws_s3_bucket" "website" {
  bucket = local.bucket_id
  acl    = "private"
  // See http://amzn.to/2Fa04ul
  policy = <<POLICY
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Sid":"AddPerm",
      "Effect":"Allow",
      "Principal": {
        "AWS":"*"
      },
      "Action":["s3:GetObject"],
      "Resource":["arn:aws:s3:::${local.bucket_id}/*"]
    }
  ]
}
POLICY

  website {
    index_document = "index.html"
  }
}

resource "aws_s3_bucket_object" "website" {
  for_each = fileset("${var.base_dir}/s3objects/", "*")
  bucket = aws_s3_bucket.website.id
  key = each.value
  acl = "public-read"
  source = "${var.base_dir}/s3objects/${each.value}"
  etag = filemd5("${var.base_dir}/s3objects/${each.value}")
}

