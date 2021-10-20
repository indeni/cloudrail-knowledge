
resource "aws_default_subnet" "def1" {
  availability_zone = "us-east-1a"
}

resource "aws_default_subnet" "def2" {
  availability_zone = "us-east-1b"
}

resource "aws_eks_cluster" "test" {
  name = "test"
  role_arn = aws_iam_role.eks-cluster-role.arn
  vpc_config {
    subnet_ids = [aws_default_subnet.def1.id, aws_default_subnet.def2.id]
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

resource "aws_iam_role_policy_attachment" "attach-eks-policy-to-eks-cluster-role" {
  role       = aws_iam_role.eks-cluster-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}