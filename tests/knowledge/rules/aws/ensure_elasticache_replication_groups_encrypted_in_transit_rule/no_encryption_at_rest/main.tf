provider "aws" {
  region = "us-east-1"
}

resource "aws_elasticache_replication_group" "cloudrail" {
  automatic_failover_enabled    = true
  availability_zones            = ["us-east-1a", "us-east-1b"]
  replication_group_id          = "tf-rep-group-1-non-encrypted"
  replication_group_description = "Non encrypted"
  node_type                     = "cache.m4.large"
  number_cache_clusters         = 2
}
