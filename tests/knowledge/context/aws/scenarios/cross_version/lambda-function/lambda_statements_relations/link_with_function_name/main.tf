
data "aws_caller_identity" "current" {}

resource "aws_lambda_function" "example" {
   function_name = "ServerlessExample"
   filename = "example.zip"
   handler = "main.handler"
   runtime = "nodejs10.x"
   role = aws_iam_role.lambda_exec.arn
}


resource "aws_iam_role" "lambda_exec" {
   name = "serverless_example_lambda"

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

resource "aws_iam_policy" "lambda_policy" {
  name        = "test_lambda_policy"
  description = "test_lambda_policy"

  policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "*",
     "Effect": "Allow",
     "Resource": "*"
   },
   {
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents"
     ],
     "Effect": "Allow",
     "Resource": "*"
   }
 ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "terraform_lambda_iam_policy_basic_execution" {
 role = aws_iam_role.lambda_exec.id
 policy_arn = aws_iam_policy.lambda_policy.arn
}


resource "aws_lambda_permission" "lambda_resource_policy" {
  statement_id = "AllowExecution1"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.example.function_name
  principal = data.aws_caller_identity.current.account_id
} 
