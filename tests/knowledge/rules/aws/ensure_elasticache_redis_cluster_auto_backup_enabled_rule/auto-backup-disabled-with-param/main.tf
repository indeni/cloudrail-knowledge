
resource "aws_elasticache_cluster" "test" {
  cluster_id               = "cluster-test-bck-disabled"
  engine                   = "redis"
  node_type                = "cache.m4.large"
  num_cache_nodes          = 1
  parameter_group_name     = "default.redis3.2"
  engine_version           = "3.2.10"
  port                     = 6379
  snapshot_retention_limit = 0
}
