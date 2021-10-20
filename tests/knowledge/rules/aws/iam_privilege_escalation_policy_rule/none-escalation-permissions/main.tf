provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "user-1" {
  name = "user-1"
  path = "/system/"

}

resource "aws_iam_user_policy" "allow-policy" {
  name = "allow-policy"
  user = aws_iam_user.user-1.name

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "iam:ListRoles"
        ],
        "Effect": "Allow",
        "Resource": "*"
      }
    ]
  }
  EOF
}
