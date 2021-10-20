resource "aws_default_vpc" "default" {
  tags = {
    Name = "default-vpc"
  }
}

data "aws_iam_policy_document" "iam_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "s3-role" {
  name = "s3-role"
  assume_role_policy = data.aws_iam_policy_document.iam_assume_policy.json

}

resource "aws_iam_policy" "attached-s3-policy" {
  name        = "s3-policy"
  description = "A test policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "policy-attachment" {
  role       = aws_iam_role.s3-role.name
  policy_arn = aws_iam_policy.attached-s3-policy.arn
}