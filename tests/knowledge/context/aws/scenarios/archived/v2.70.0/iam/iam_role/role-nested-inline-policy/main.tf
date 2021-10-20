
data "aws_iam_policy_document" "iam_assume_role_policy_doc"{
  version = "2012-10-17"

  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "sts:AssumeRole",
    ]
    principals {
      type = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2-role" {
  name = "ec2-role"
  assume_role_policy = data.aws_iam_policy_document.iam_assume_role_policy_doc.json
}

resource "aws_iam_role_policy" "ec2-describe-policy" {
  name = "ec2-describe-policy"
  role = aws_iam_role.ec2-role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:Describe*",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}