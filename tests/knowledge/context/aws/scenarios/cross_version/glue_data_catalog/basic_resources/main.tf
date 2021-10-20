resource "aws_glue_catalog_database" "cloudrail_table_database" {
  name = "cloudrail_table_database"
}

resource "aws_glue_catalog_table" "cloudrail_table" {
  name          = "cloudrail_table"
  database_name = aws_glue_catalog_database.cloudrail_table_database.name
}

resource "aws_iam_role" "cloudrail_glue_iam" {
  name = "cloudrail_glue_iam"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_s3_bucket" "cloudrail" {
  bucket = "cloudrail-glue"
  acl    = "private"
}

resource "aws_glue_crawler" "cloudrail_table_crawler" {
  database_name = aws_glue_catalog_database.cloudrail_table_database.name
  name          = "cloudrail_table_crawler"
  role          = aws_iam_role.cloudrail_glue_iam.arn

  s3_target {
    path = "s3://${aws_s3_bucket.cloudrail.bucket}"
  }
}
