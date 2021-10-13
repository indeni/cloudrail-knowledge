

resource "aws_iam_user" "non_console_user" {
  name = "not_console_user"
}

resource "aws_iam_user_policy_attachment" "attach-user-policy" {
  user       = aws_iam_user.non_console_user.name
  policy_arn = "arn:aws:iam::aws:policy/SecurityAudit"
}

resource "aws_iam_policy_attachment" "test-attach" {
  name       = "test-attachment"
  users      = [aws_iam_user.non_console_user.name]
  policy_arn = "arn:aws:iam::aws:policy/SecurityAudit"
}
