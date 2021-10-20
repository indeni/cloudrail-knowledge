resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${local.nameB}-ECSCluster"
}
