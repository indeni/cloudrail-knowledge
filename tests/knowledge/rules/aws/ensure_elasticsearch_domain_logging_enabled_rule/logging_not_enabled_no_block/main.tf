provider "aws" {
  region = "us-east-1"
}

resource "aws_elasticsearch_domain" "test" {
  domain_name           = "domain-logging-test"
  elasticsearch_version = "5.1"

  cluster_config {
    instance_type = "i3.large.elasticsearch"
  }

}

resource "aws_cloudwatch_log_group" "test" {
  name = "test-log-group"
}

resource "aws_cloudwatch_log_resource_policy" "example" {
  policy_name = "example"

  policy_document = <<CONFIG
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "es.amazonaws.com"
      },
      "Action": [
        "logs:PutLogEvents",
        "logs:PutLogEventsBatch",
        "logs:CreateLogStream"
      ],
      "Resource": "arn:aws:logs:*"
    }
  ]
}
CONFIG
}
