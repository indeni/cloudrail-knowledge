provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "user-1" {
  name = "user-1"
}

resource "aws_iam_group" "developers" {
  name = "developers"
}

resource "aws_iam_group_policy" "developers-group-policy" {
  name  = "developers-group-policy"
  group = aws_iam_group.developers.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:Describe*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_group_membership" "developers-team" {
  name = "developers-team"

  users = [
    aws_iam_user.user-1.name
  ]

  group = aws_iam_group.developers.name
}
