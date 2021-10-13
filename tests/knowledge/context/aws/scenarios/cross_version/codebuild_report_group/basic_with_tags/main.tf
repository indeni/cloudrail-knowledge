
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_kms_key" "by_alias" {
  key_id = "alias/aws/s3"
}

resource "aws_s3_bucket" "codebuild-report" {
  bucket = "codebuild-report-group-non-kms-cmk-encrypted"
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "codebuild-report" {
  bucket                  = aws_s3_bucket.codebuild-report.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_codebuild_report_group" "non-encrypted" {
  name = "codebuild-report-group-non-kms-cmk-encrypted"
  type = "TEST"
  tags = {
    NAme = "Project-cloudrail"
  }

  export_config {
    type = "S3"

    s3_destination {
      bucket              = aws_s3_bucket.codebuild-report.id
      encryption_disabled = false
      encryption_key      = data.aws_kms_key.by_alias.arn
      packaging           = "NONE"
      path                = "/some"
    }
  }
}
