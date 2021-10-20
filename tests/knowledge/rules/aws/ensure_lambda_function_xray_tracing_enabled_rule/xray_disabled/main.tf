provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "test" {
  name = "cloudrail-test-iam_for_lambda"

  assume_role_policy = <<-EOF
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

resource "aws_lambda_function" "test" {
  filename         = "${path.module}/example_lambda_code/golang-example.zip"
  function_name    = "golang-example"
  handler          = "main"
  role             = aws_iam_role.test.arn
  source_code_hash = filebase64sha256("${path.module}/example_lambda_code/golang-example.zip")
  runtime          = "go1.x"

  environment {
    variables = {
      foo = "bar"
    }
  }
}
