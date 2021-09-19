
resource "aws_elasticsearch_domain" "test" {
  domain_name = "test"
  tags = {
    Name = "Cloudrail ES tags"
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 10
    volume_type = "gp2"
  }
}
