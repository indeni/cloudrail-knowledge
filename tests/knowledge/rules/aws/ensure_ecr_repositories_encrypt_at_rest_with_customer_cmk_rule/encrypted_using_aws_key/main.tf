data "aws_kms_key" "by_alias" {
  key_id = "alias/aws/ecr"
}

resource "aws_ecr_repository" "test" {
  name                 = "cloudrail-test-encrypted"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = data.aws_kms_key.by_alias.arn
  }
}
