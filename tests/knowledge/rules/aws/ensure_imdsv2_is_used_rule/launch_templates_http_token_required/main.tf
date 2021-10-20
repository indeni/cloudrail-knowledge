provider "aws" {
  region = "us-east-1"
}

locals {
  test_name = "test http_tokens launch template - required"
}

resource "aws_launch_template" "launch_template_test" {
  name = "launch_template_test"

  block_device_mappings {
    device_name = "/dev/sda1"
    ebs {
      volume_size = 20
    }
  }

  capacity_reservation_specification {
    capacity_reservation_preference = "open"
  }

  cpu_options {
    core_count       = 4
    threads_per_core = 2
  }

  credit_specification {
    cpu_credits = "standard"
  }
  disable_api_termination = true
  ebs_optimized = true
  
  elastic_gpu_specifications {
    type = "test"
  }

  elastic_inference_accelerator {
    type = "eia1.medium"
  }

  image_id = "ami-022f8e8ca7e5665d7"
  instance_initiated_shutdown_behavior = "terminate"

  instance_market_options {
    market_type = "spot"
  }

  instance_type = "t2.micro"

  license_specification {
    license_configuration_arn = "arn:aws:license-manager:us-east-1:123456789012:license-configuration:lic-0123456789abcdef0123456789abcdef"
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  monitoring {
    enabled = true
  }

  network_interfaces {
    associate_public_ip_address = true
  }

  placement {
    availability_zone = "us-east-2a"
  }

  vpc_security_group_ids = ["sg-12345678"]

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "test"
    }
  }
}