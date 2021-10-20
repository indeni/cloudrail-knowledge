

resource "aws_sns_topic" "cloudrail_1" {
  name              = "sns_not_ecnrypted-1"
  tags = {
    Name = "Sns Topic Cloudrail Test"
  }
}
