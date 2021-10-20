
resource "aws_iam_user" "iam_user_1" {
  name = "iam_user_1"
  tags = {
    Name = "ecs-cluster-test"
    Env = "Cloudrail"
  }
}