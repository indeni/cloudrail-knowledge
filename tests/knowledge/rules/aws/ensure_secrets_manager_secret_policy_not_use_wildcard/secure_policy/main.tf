provider "aws" {
  region = "us-east-1"
}

resource "aws_secretsmanager_secret" "secure_policy" {
  name = "secure_secret_1"
}

resource "aws_secretsmanager_secret_policy" "example" {
  secret_arn = aws_secretsmanager_secret.secure_policy.arn

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnableAllPermissions",
      "Effect": "Allow",
      "Principal": {
          "AWS": "arn:aws:iam::111111111111:root"
      },
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:ListSecrets"
        ],
      "Resource": "*"
    }
  ]
}
POLICY
}