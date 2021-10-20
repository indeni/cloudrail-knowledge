provider "aws" {
  region = "us-east-1"
}

resource "aws_elasticsearch_domain" "example" {
  domain_name           = "cloudrail-non-enc-in-tran"
  elasticsearch_version = "5.5"

  cluster_config {
    instance_type = "i3.large.elasticsearch"
  }

}