resource "aws_sns_topic" "cloudrail" {
  name              = "sns_ecnrypted"
  kms_master_key_id = "alias/aws/sns"
}
