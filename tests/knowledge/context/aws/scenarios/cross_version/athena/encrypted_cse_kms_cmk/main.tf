
resource "aws_kms_key" "athena_workgroup" {
  description             = "KMS key for athena workgroup"
  deletion_window_in_days = 7
}

resource "aws_s3_bucket" "cloudrail_anthena_bucket" {
  bucket = "cloudrail-wg-encrypted-cse-kms-cmk"
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "cloudrail_anthena_bucket" {
  bucket                  = aws_s3_bucket.cloudrail_anthena_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_athena_workgroup" "cloudrail_wg" {
  name = "cloudrail-wg-encrypted-cse-kms-cmk"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://{aws_s3_bucket.cloudrail_anthena_bucket.bucket}/output/"

      encryption_configuration {
        encryption_option = "CSE_KMS"
        kms_key_arn       = aws_kms_key.athena_workgroup.arn # "arn:aws:kms:<REGION>:<ACCOUNT-ID>:alias/<NAME>"
      }
    }
  }
}
