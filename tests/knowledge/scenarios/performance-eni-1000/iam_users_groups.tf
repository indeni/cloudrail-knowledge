resource "aws_iam_user" "test" {
  count = local.iam_users_number
  name  = "test-${count.index}"
}

resource "aws_iam_user_policy" "test" {
  count = local.iam_users_number
  name  = "test-${count.index}"
  user  = aws_iam_user.test[count.index].name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:*",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_group" "test" {
  count = local.iam_groups_number
  name  = "test-${count.index}"
}

resource "aws_iam_group_policy" "test" {
  count = local.iam_groups_number
  name  = "test-${count.index}"
  group = aws_iam_group.test[count.index].name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:Describe*",
          "iam:*",
          "s3:*",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_group_membership" "test" {
  count = local.iam_groups_number
  name  = "test-${count.index}"
  group = aws_iam_group.test[count.index].name
  users = aws_iam_user.test.*.name
}
