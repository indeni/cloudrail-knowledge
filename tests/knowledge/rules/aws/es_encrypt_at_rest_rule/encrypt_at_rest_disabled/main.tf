provider "aws" {
  region = "us-east-1"
}

resource "aws_elasticsearch_domain" "test" {
  domain_name = "test"
  elasticsearch_version = "7.10"

  ebs_options {
    ebs_enabled = true
    volume_size = 10
    volume_type = "gp2"
  }
  encrypt_at_rest {
    enabled    = false
  }
}
