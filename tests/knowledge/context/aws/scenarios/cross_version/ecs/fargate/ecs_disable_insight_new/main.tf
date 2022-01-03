
resource "aws_ecs_cluster" "test" {
  name = "ecs-insights-test"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}
