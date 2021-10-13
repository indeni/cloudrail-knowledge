
resource "aws_ecr_repository" "test" {
  name = "cloudrail-test-on-push-enabled"

  image_scanning_configuration {
    scan_on_push = true
  }
}
