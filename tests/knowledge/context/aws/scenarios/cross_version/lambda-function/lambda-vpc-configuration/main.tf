resource "aws_lambda_function" "my-lambda" {
  filename = "lambda.zip"
  function_name = "my-lambda"
  role          = aws_iam_role.lambda-role.arn
  handler       = "lambda_function.lambda_handler"
  runtime = "python3.8"

  vpc_config {
    security_group_ids = [aws_security_group.allow-http.id]
    subnet_ids = [aws_subnet.private-subnet.id]
  }


}

resource "aws_iam_role" "lambda-role" {
  name = "lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "user-1-policy" {
  name        = "user-1-policy"
  description = "A test policy"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Id": "default",
  "Statement": [
    {
      "Sid": "somesid",
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "policy-attachment" {
  role       = aws_iam_role.lambda-role.name
  policy_arn = aws_iam_policy.user-1-policy.arn
}



resource "aws_vpc" "main" {
  cidr_block = "192.168.100.0/24"
}


resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "192.168.100.128/25"

  tags = {
    Name = "private-subnet-test"
  }
}

resource "aws_security_group" "allow-http" {
  vpc_id      = aws_vpc.main.id
  description = "allow http"
  name = "security-group-test"
  ingress {
    from_port = 80
    protocol = "TCP"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}