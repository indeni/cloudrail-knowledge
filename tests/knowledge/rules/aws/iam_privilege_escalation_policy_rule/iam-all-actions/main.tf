provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "role" {
  name = "role"

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

  inline_policy {
    name = "allow-all-actions"
    policy = <<-EOF
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Action": [
              "*"
            ],
            "Effect": "Allow",
            "Resource": "*"
          }
        ]
      }
      EOF
  }
}
