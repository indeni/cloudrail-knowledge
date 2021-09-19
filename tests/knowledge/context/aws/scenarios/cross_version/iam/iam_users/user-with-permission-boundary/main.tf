resource "aws_iam_user" "test-user" {
  name = "test-user"

  permissions_boundary = aws_iam_policy.pb_policy.arn
}

resource "aws_iam_policy" "pb_policy" {
  name        = "permission_boundary_policy"
  path        = "/"
  description = "Permission Boundary Policy - restricts 'ec2-role' from doing DescribeInstances"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:DescribeInstances"
      ],
      "Effect": "Deny",
      "Resource": "*"
    },
    {
      "Action": [
        "ec2:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}