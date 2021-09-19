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

resource "aws_lambda_permission" "allow-s3-bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my-lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket.arn
  source_account = "111111111111"
  qualifier     = aws_lambda_alias.my-lambda-alias.name
}

resource "aws_lambda_alias" "my-lambda-alias" {
  name             = "v1"
  description      = "a sample description"
  function_name    = aws_lambda_function.my-lambda.arn
  function_version = "$LATEST"
}

resource "aws_s3_bucket" "bucket" {
  bucket = "delete-me-eu-central-1-3214213"
}
