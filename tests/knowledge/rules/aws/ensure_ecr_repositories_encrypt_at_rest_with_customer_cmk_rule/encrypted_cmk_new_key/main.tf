resource "aws_kms_key" "test" {
  description             = "KMS key for ECR"
  deletion_window_in_days = 7
}

resource "aws_ecr_repository" "test" {
  name                 = "cloudrail-test-encrypted"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.test.arn
  }
}
