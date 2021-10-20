resource "aws_ecr_repository" "test" {
  name                 = "cloudrail-test-immutable"
  image_tag_mutability = "IMMUTABLE"
}
