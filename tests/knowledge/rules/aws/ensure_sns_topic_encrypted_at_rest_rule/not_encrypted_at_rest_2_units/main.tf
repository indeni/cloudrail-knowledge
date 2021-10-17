provider "aws" {
  region = "us-east-1"
}

resource "aws_sns_topic" "cloudrail_1" {
  name              = "sns_not_ecnrypted-1"
}

resource "aws_sns_topic" "cloudrail_2" {
  name              = "sns_not_ecnrypted-2"
}