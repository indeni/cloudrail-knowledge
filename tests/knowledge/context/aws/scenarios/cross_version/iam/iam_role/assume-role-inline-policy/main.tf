resource "aws_default_vpc" "default" {
  tags = {
    Name = "default-vpc"
  }
}

data "aws_iam_policy_document" "iam_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "role" {
  name = "ec2-assume-role"
  assume_role_policy = data.aws_iam_policy_document.iam_assume_policy.json

}