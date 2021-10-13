resource "aws_vpc" "nondefault" {
  cidr_block = "10.1.1.0/24"
}

resource "aws_security_group" "nondefault" {
  vpc_id = aws_vpc.nondefault.id
}

resource "aws_subnet" "nondefault_1" {
  vpc_id = aws_vpc.nondefault.id
  cidr_block = "10.1.1.128/25"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "nondefault_2" {
  vpc_id = aws_vpc.nondefault.id
  cidr_block = "10.1.1.0/25"
  availability_zone = "us-east-1c"
}

resource "aws_elasticsearch_domain" "test" {
  domain_name = "test"

  vpc_options {
    subnet_ids = [
      aws_subnet.nondefault_1.id,
      aws_subnet.nondefault_2.id]
    security_group_ids = [aws_security_group.nondefault.id]
  }

  domain_endpoint_options {
    enforce_https = true
    tls_security_policy  = "Policy-Min-TLS-1-0-2019-07"
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 10
    volume_type = "gp2"
  }

  cluster_config {
    instance_type = "t2.micro.elasticsearch"
    instance_count = 2
    zone_awareness_enabled = true
    #If you ignore it you'll get: Error creating ElasticSearch domain: ValidationException: You must specify exactly one subnet
    #Notice that there is no "=" Below - or you'll visit this thread: https://github.com/terraform-providers/terraform-provider-aws/issues/12365
  }
}
