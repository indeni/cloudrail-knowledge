resource "aws_sqs_queue" "not-secure-q" {
  name = "cloudrail-not-secure-queue"
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqs-secure-policy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:*"
    }
  ]
}
POLICY
}
