
data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "s3-bucket-policy" {
  version = "2012-10-17"
  statement {
    sid = "FullAccess"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [data.aws_caller_identity.current.account_id]
    }
    actions   = ["s3:*"]
    resources = ["arn:aws:s3:::cloudrail-testing-bucket"]
  }
}


resource "aws_s3_bucket" "test-bucket" {
  bucket = "cloudrail-testing-bucket"
  policy = data.aws_iam_policy_document.s3-bucket-policy.json
}

data "aws_iam_policy_document" "iam_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "s3-bucket-role" {
  name = "s3-bucket-role"
  assume_role_policy = data.aws_iam_policy_document.iam_assume_policy.json
}


resource "aws_iam_policy" "policy" {
  name        = "allow_role_s3_operations"
  description = "allow_role_s3_operations"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "s3:Describe*"
        ],
        "Effect": "Allow",
        "Resource": "*"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy_attachment" "attach-policy-to-s3-bucket-role" {
  role       = aws_iam_role.s3-bucket-role.name
  policy_arn = aws_iam_policy.policy.arn
}