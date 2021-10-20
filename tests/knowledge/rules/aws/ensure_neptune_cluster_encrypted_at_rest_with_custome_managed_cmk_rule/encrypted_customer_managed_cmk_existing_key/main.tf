provider "aws" {
  region = "us-east-1"
}

data "aws_kms_key" "by_alias" {
  key_id = "alias/test-rds"
}

resource "aws_neptune_cluster" "test" {
  cluster_identifier  = "cloudrail-test-encrypted"
  engine              = "neptune"
  skip_final_snapshot = true
  apply_immediately   = true
  storage_encrypted   = true
  kms_key_arn         = data.aws_kms_key.by_alias.arn
}
