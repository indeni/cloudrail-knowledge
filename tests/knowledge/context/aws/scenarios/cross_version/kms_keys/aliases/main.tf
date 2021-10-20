resource "aws_kms_key" "cloudrail-test" {}

resource "aws_kms_alias" "a" {
  name          = "alias/cloudrail-alias"
  target_key_id = aws_kms_key.cloudrail-test.key_id
}