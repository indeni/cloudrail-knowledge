locals {
  region  = "us-east-1"
  vpc_cidr_block = "192.168.14.0/24"
  cidr_block_1 = "192.168.14.128/26"
  cidr_block_2 = "192.168.14.192/26"
}

resource "aws_vpc" "test-vpc" {
  cidr_block = local.vpc_cidr_block
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.test-vpc.id
  cidr_block = local.cidr_block_1
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "private-subnet_2" {
  vpc_id     = aws_vpc.test-vpc.id
  cidr_block = local.cidr_block_2
  availability_zone = "us-east-1b"
}

resource "aws_eks_cluster" "my-eks-cluster" {
  name     = "example"
  role_arn = aws_iam_role.eks-cluster-role.arn

  vpc_config {
    subnet_ids = [
      aws_subnet.private-subnet.id,
      aws_subnet.private-subnet_2.id
    ]
  }

}

resource "aws_iam_role" "eks-cluster-role" {
  name = "eks-cluster-role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_policy" "policy" {
  name        = "allow_role_eks_operations"
  description = "allow_role_eks_operations"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "NotAction": [
          "eks:StartJobRun"
        ],
        "Effect": "Allow",
        "Resource": "*"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy_attachment" "attach-policy-to-eks-cluster-role" {
  role       = aws_iam_role.eks-cluster-role.name
  policy_arn = aws_iam_policy.policy.arn
}

resource "aws_iam_role_policy_attachment" "attach-eks-policy-to-eks-cluster-role" {
  role       = aws_iam_role.eks-cluster-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}