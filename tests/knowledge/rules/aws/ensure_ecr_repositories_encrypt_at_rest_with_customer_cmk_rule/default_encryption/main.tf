resource "aws_ecr_repository" "test" {
  name                 = "cloudrail-test-encrypted"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
  }
}
