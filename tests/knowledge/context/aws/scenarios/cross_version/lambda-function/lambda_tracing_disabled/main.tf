
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

resource "aws_lambda_function" "my-lambda" {
  filename         = "lambda.zip"
  function_name    = "my-lambda"
  handler          = "main"
  role             = aws_iam_role.test.arn
  runtime          = "python3.8"

  environment {
    variables = {
      foo = "bar"
    }
  }
}
