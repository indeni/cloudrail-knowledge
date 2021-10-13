
resource "aws_neptune_cluster" "test-tags" {
  cluster_identifier  = "cloudrail-test-encrypted"
  engine              = "neptune"
  skip_final_snapshot = true
  apply_immediately   = true
  storage_encrypted   = true
  tags = {
    Name = "testing-tags",
    Env = "Cloudrail Rocks",
    Type = "Neptune_cluster"
  }
}

resource "aws_neptune_cluster_instance" "test-tags" {
  count              = 1
  cluster_identifier = aws_neptune_cluster.test-tags.id
  engine             = "neptune"
  instance_class     = "db.r4.large"
  apply_immediately  = true
  tags = {
    Name = "testing-tags",
    Env = "Cloudrail Rocks",
    Type = "Neptune_instance"
  }
}