provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role_policy" "test_policy" {
  name = "test_policy"
  role = aws_iam_role.iam_for_cloudwatch.id

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "kinesis:PutRecord"
        ],
        "Effect": "Allow",
        "Resource": "${aws_kinesis_stream.kinesis_for_cloudwatch.arn}"
      }
    ]
  }
  EOF
}

resource "aws_iam_role" "iam_for_cloudwatch" {
  name = "iam_for_cloudwatch"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "logs.us-east-1.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }
  EOF
}

resource "aws_kinesis_stream" "kinesis_for_cloudwatch" {
  name             = "kinesis_for_cloudwatch"
  shard_count      = 1
  retention_period = 48

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]
}

resource "aws_cloudwatch_log_destination" "test_destination" {
  name       = "test_destination"
  role_arn   = aws_iam_role.iam_for_cloudwatch.arn
  target_arn = aws_kinesis_stream.kinesis_for_cloudwatch.arn
}
