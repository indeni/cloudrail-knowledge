provider "aws" {
  region = "us-east-1"
}


resource "aws_sqs_queue_policy" "secure-policy" {
  queue_url = "https://sqs.us-east-1.amazonaws.com/115553109071/cloudrail-secure-queue_2"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqs-secure-policy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": {
          "AWS": "arn:aws:iam::111111111111:root"
      },
      "Action": "sqs:SendMessage",
      "Resource": "https://sqs.us-east-1.amazonaws.com/115553109071/cloudrail-secure-queue_2"
    }
  ]
}
POLICY
}
