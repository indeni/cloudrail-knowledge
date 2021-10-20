
resource "aws_sqs_queue" "cloudrail" {
  name = "sqs_non_encrypted"
  tags = {
    Name = "Sqs Cloudrail Test"
  }
}
