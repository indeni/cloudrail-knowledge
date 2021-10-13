
data "aws_redshift_service_account" "main" {}

data "aws_iam_policy_document" "logging" {
  version = "2012-10-17"
  statement {
    sid    = "Enable Redshift logging"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [data.aws_redshift_service_account.main.arn]
    }
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.logging.arn}/*"]
  }
  statement {
    sid    = "Enable Redshift Get Bucket ACL"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [data.aws_redshift_service_account.main.arn]
    }
    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.logging.arn]
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

resource "aws_redshift_cluster" "test" {
  cluster_identifier  = "cloudrail-redshift-cluster-logging"
  database_name       = "mydb"
  master_username     = "administrator"
  master_password     = "Zasdf8adf887"
  node_type           = "dc1.large"
  cluster_type        = "single-node"
  skip_final_snapshot = true

  logging {
    enable      = true
    bucket_name = aws_s3_bucket.logging.id
    s3_key_prefix = "test-prefix"
  }
}
