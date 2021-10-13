resource "aws_kms_key" "test" {
  description             = "KMS key for CodeBuild Project"
  deletion_window_in_days = 7
}

resource "aws_kms_alias" "test" {
  name          = "alias/testing-codebuild"
  target_key_id = aws_kms_key.test.key_id
}
