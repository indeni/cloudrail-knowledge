provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "non_console_user" {
  name = "not_console_user"
}

resource "aws_iam_group" "group" {
  name = "test-policy-group"
}

resource "aws_iam_policy_attachment" "test-attach" {
  name       = "test-attachment"
  groups     = [aws_iam_group.group.name]
  policy_arn = "arn:aws:iam::aws:policy/SecurityAudit"
}
