resource "aws_sqs_queue" "test" {
  name = "sqs_non_encrypted"
}

resource "aws_sqs_queue_policy" "test" {
  queue_url = aws_sqs_queue.test.id

  policy = <<-POLICY
    {
        "Version": "2012-10-17",
        "Id": "sqspolicy",
        "Statement": [
            {
                "Sid": "First",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "sqs:SendMessage",
                "Resource": "${aws_sqs_queue.test.arn}"
            }
        ]
    }
    POLICY
}
