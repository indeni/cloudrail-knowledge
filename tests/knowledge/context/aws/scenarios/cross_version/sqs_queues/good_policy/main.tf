resource "aws_sqs_queue" "secure-q" {
  name = "cloudrail-secure-queue"
}

resource "aws_sqs_queue_policy" "secure-policy" {
  queue_url = aws_sqs_queue.secure-q.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqs-secure-policy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.secure-q.arn}"
    }
  ]
}
POLICY
}
