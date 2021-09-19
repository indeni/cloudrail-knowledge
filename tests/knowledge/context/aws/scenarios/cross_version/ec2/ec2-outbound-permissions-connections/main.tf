locals {
  region  = "us-east-1"
  https_port = 443
  max_port = 65535
  cidr_block = "192.168.100.128/25"
  zero_cidr_block = "0.0.0.0/0"
  s3_prefix_list_cidr_block = "54.231.0.0/17"
}

data "aws_caller_identity" "current" {}

resource "aws_iam_role" "s3-full-access-role" {
  name = "s3-full-access-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "AWS": "*"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "policy" {
  name        = "allow_role_s3_operations"
  description = "allow_role_s3_operations"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "s3:*"
        ],
        "Effect": "Allow",
        "Sid": "",
        "Resource": "*"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy_attachment" "attach-policy-to-s3-bucket-role" {
  role       = aws_iam_role.s3-full-access-role.name
  policy_arn = aws_iam_policy.policy.arn
}

resource "aws_vpc" "main" {
  cidr_block = "192.168.100.0/24"
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = local.cidr_block
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-subnet"
  }
}

resource "aws_route_table" "private-subnet-rtb" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "test-rt"
  }
}

resource "aws_vpc_endpoint_route_table_association" "example" {
  route_table_id  = aws_route_table.private-subnet-rtb.id
  vpc_endpoint_id = aws_vpc_endpoint.s3-vpc-endpoint.id
}

resource "aws_route_table_association" "public-subnet-rt-assoc" {
  subnet_id      = aws_subnet.private-subnet.id
  route_table_id = aws_route_table.private-subnet-rtb.id
}

resource "aws_security_group" "allow-https" {
  vpc_id = aws_vpc.main.id
  description = "allow https"
  ingress {
    from_port = local.https_port
    protocol = "tcp"
    to_port = local.https_port
    cidr_blocks = [local.zero_cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_subnet.private-subnet.cidr_block]
  }
}

resource "aws_security_group" "allow-all-local" {
  description = "allow-all-local"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_subnet.private-subnet.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_subnet.private-subnet.cidr_block]
  }
}

resource "aws_vpc_endpoint" "s3-vpc-endpoint" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.${local.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids = [aws_route_table.private-subnet-rtb.id]

}

resource "aws_s3_bucket" "test-bucket" {
  bucket = "atotalyrandomname929293"
  policy =  <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "s3:GetBucketLocation",
      "Effect": "Deny",
      "Sid": "DenyS3Describe",
      "Principal": {
          "AWS": "${data.aws_caller_identity.current.account_id}"
      },
      "Resource": "arn:aws:s3:::atotalyrandomname929293"
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "ec2-web-server-profile" {
  name = "ec2-web-server-profile"
  role = aws_iam_role.s3-full-access-role.name
}

resource "aws_instance" "ec2-web-server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id = aws_subnet.private-subnet.id
  vpc_security_group_ids = [aws_security_group.allow-https.id, aws_security_group.allow-all-local.id]
  iam_instance_profile = aws_iam_instance_profile.ec2-web-server-profile.name
  tags = {
    Name = "ec2-web-server"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}