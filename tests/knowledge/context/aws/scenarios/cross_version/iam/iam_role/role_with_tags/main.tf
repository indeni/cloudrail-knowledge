resource "aws_iam_role" "ec2-role" {
  name = "ec2-role"
  tags = {
    Name = "ec2-role-test",
    Env = "Cloudrail"
  }
  assume_role_policy = jsonencode({
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
    })
}

resource "aws_iam_role_policy" "ec2-describe-policy" {
  name = "ec2-describe-policy"
  role = aws_iam_role.ec2-role.id

  policy = <<-EOF
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