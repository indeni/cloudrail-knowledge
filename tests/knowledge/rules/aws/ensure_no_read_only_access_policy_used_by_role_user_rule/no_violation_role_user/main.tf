provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "non_console_user" {
  name = "not_console_user"
}

resource "aws_iam_role" "role" {
  name = "test-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach-role-policy" {
  role       = aws_iam_role.role.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}

resource "aws_iam_user_policy_attachment" "attach-user-policy" {
  user       = aws_iam_user.non_console_user.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}
