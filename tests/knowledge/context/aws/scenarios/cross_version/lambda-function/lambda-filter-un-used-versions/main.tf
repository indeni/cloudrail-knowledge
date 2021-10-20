
resource "aws_lambda_function" "my-lambda" {
  filename = "lambda.zip"
  function_name = "my-lambda"
  role          = aws_iam_role.lambda-role.arn
  handler       = "lambda_function.lambda_handler"
  runtime = "python3.8"
}

resource "aws_lambda_function" "my-lambda-without-alias" {
  filename = "lambda.zip"
  function_name = "my-lambda-without-alias"
  role          = aws_iam_role.lambda-role.arn
  handler       = "lambda_function.lambda_handler"
  runtime = "python3.8"
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

resource "aws_lambda_alias" "my-lambda-alias" {
  name             = "v1"
  description      = "a sample description"
  function_name    = aws_lambda_function.my-lambda.function_name
  function_version = "$LATEST"
}
