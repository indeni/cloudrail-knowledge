resource "aws_lambda_function" "my-lambda" {
  filename       = "lambda.zip"
  function_name = "my-lambda"
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

resource "aws_lambda_permission" "allow-user-1" {
  statement_id  = "AllowUser1Execution"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my-lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_iam_role.lambda-role.arn
  qualifier     = aws_lambda_alias.my-lambda-alias.name
}

resource "aws_lambda_alias" "my-lambda-alias" {
  name             = "v1"
  description      = "a sample description"
  function_name    = aws_lambda_function.my-lambda.arn
  function_version = "$LATEST"
}

resource "aws_iam_user" "user-1" {
  name = "user-1"
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
      "Sid": "",
      "Effect": "Allow",
      "Action": ["lambda:InvokeFunction"],
      "Resource": ["${aws_lambda_function.my-lambda.arn}:v1"]
    }
  ]
}
EOF
}

resource "aws_iam_user_policy_attachment" "user-1-attach" {
  user       = aws_iam_user.user-1.name
  policy_arn = aws_iam_policy.user-1-policy.arn
}