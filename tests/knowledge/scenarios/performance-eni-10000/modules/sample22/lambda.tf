resource "aws_s3_bucket" "code" {
  acl = "private"
}

resource "aws_s3_bucket_object" "file" {
  bucket = aws_s3_bucket.code.id
  key    = "v1.0.0/code.zip"
  source = "./code-example/code.zip"
}

module "lambda_sg_serverlessProduction" {
  count               = local.projects["serverlessProduction"].num_lambdas
  source              = "terraform-aws-modules/security-group/aws//modules/web"
  version             = "3.17.0"
  name                = "lambda-sg-prod-${count.index}"
  description         = "Security group for Lambdas"
  vpc_id              = module.serverlessProduction.vpc_id
  ingress_cidr_blocks = module.serverlessProduction.public_subnets_cidr_blocks
}

module "lambda_sg_serverlessStaging" {
  count               = local.projects["serverlessStaging"].num_lambdas
  source              = "terraform-aws-modules/security-group/aws//modules/web"
  version             = "3.17.0"
  name                = "lambda-sg-stag-${count.index}"
  description         = "Security group for Lambdas"
  vpc_id              = module.serverlessStaging.vpc_id
  ingress_cidr_blocks = module.serverlessStaging.public_subnets_cidr_blocks
}

module "lambda_sg_serverlessTesting" {
  count               = local.projects["serverlessTesting"].num_lambdas
  source              = "terraform-aws-modules/security-group/aws//modules/web"
  version             = "3.17.0"
  name                = "lambda-sg-test-${count.index}"
  description         = "Security group for Lambdas"
  vpc_id              = module.serverlessTesting.vpc_id
  ingress_cidr_blocks = module.serverlessTesting.public_subnets_cidr_blocks
}

resource "aws_iam_role" "lambda_exec_prod" {
  count = local.projects["serverlessProduction"].num_lambdas
  name  = "lambda-role-prod-${count.index}"

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

resource "aws_iam_role_policy_attachment" "AWSLambdaVPCAccessExecutionRole_prod" {
  count      = local.projects["serverlessProduction"].num_lambdas
  role       = aws_iam_role.lambda_exec_prod[count.index].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_lambda_function" "prod" {
  count         = local.projects["serverlessProduction"].num_lambdas
  function_name = "function-prod-${count.index}"
  s3_bucket     = aws_s3_bucket.code.id
  s3_key        = aws_s3_bucket_object.file.id
  handler       = "main.handler"
  runtime       = "nodejs10.x"
  role          = aws_iam_role.lambda_exec_prod[count.index].arn

  vpc_config {
    subnet_ids         = module.serverlessProduction.private_subnets
    security_group_ids = [module.lambda_sg_serverlessProduction[count.index].this_security_group_id]
  }
}

resource "aws_iam_role" "lambda_exec_stag" {
  count = local.projects["serverlessStaging"].num_lambdas
  name  = "lambda-role-stag-${count.index}"

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

resource "aws_iam_role_policy_attachment" "AWSLambdaVPCAccessExecutionRole_stag" {
  count      = local.projects["serverlessStaging"].num_lambdas
  role       = aws_iam_role.lambda_exec_stag[count.index].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_lambda_function" "stag" {
  count         = local.projects["serverlessStaging"].num_lambdas
  function_name = "function-stag-${count.index}"
  s3_bucket     = aws_s3_bucket.code.id
  s3_key        = aws_s3_bucket_object.file.id
  handler       = "main.handler"
  runtime       = "nodejs10.x"
  role          = aws_iam_role.lambda_exec_stag[count.index].arn

  vpc_config {
    subnet_ids         = module.serverlessStaging.private_subnets
    security_group_ids = [module.lambda_sg_serverlessStaging[count.index].this_security_group_id]
  }
}

resource "aws_iam_role" "lambda_exec_test" {
  count = local.projects["serverlessTesting"].num_lambdas
  name  = "lambda-role-test-${count.index}"

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

resource "aws_iam_role_policy_attachment" "AWSLambdaVPCAccessExecutionRole_test" {
  count      = local.projects["serverlessTesting"].num_lambdas
  role       = aws_iam_role.lambda_exec_test[count.index].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_lambda_function" "test" {
  count         = local.projects["serverlessTesting"].num_lambdas
  function_name = "function-test-${count.index}"
  s3_bucket     = aws_s3_bucket.code.id
  s3_key        = aws_s3_bucket_object.file.id
  handler       = "main.handler"
  runtime       = "nodejs10.x"
  role          = aws_iam_role.lambda_exec_test[count.index].arn

  vpc_config {
    subnet_ids         = module.serverlessTesting.private_subnets
    security_group_ids = [module.lambda_sg_serverlessTesting[count.index].this_security_group_id]
  }
}
