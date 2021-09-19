provider "aws" {
  region = "us-east-1"
}

resource "aws_sqs_queue" "not-secure-q" {
  name = "cloudrail-not-secure-queue"
}

resource "aws_sqs_queue_policy" "secure-policy" {
  queue_url = aws_sqs_queue.not-secure-q.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqs-secure-policy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:*",
      "Resource": "${aws_sqs_queue.not-secure-q.arn}"
    }
  ]
}
POLICY
}
