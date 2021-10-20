
resource "aws_ecr_repository" "not_secure_ecr" {
  name = "not_secure_ecr"
  tags = {
    Name = "Ecr Repo Cloudrail"
  }
}

resource "aws_ecr_repository_policy" "not_secure_policy" {
  repository = aws_ecr_repository.not_secure_ecr.name

  policy = <<EOF
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "new policy",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "ecr:*"
            ]
        }
    ]
}
EOF
}