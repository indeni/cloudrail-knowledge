provider "aws" {
  region                  = "eu-central-1"
}

resource "aws_iam_service_linked_role" "es" {
  aws_service_name = "es.amazonaws.com"
  description      = "Allows Amazon ES to manage AWS resources for a domain on your behalf."
}

resource "aws_elasticsearch_domain" "test" {
  domain_name = "test"

  ebs_options {
    ebs_enabled = true
    volume_size = 10
    volume_type = "gp2"
  }
}
