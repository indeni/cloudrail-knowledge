provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "group_user" {
  name = "user_in_group"
}

resource "aws_iam_group" "group" {
  name = "test-policy-group"
}

resource "aws_iam_user_group_membership" "test_group" {
  user = aws_iam_user.group_user.name

  groups = [
    aws_iam_group.group.name
  ]
}

resource "aws_iam_group_policy_attachment" "attach-group-policy" {
  group      = aws_iam_group.group.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}