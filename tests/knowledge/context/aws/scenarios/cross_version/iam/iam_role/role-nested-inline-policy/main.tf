
data "aws_iam_policy_document" "iam_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}


resource "aws_iam_role" "ec2-role" {
  name = "ec2-role"
  assume_role_policy = data.aws_iam_policy_document.iam_assume_policy.json

  inline_policy {
    name = "ec2-describe-policy"
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
}
