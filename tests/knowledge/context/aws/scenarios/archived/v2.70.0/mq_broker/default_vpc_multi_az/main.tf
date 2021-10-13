data "aws_security_group" "selected" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "group-name"
    values = ["default"]
  }
}

data "aws_vpc" "default" {
  default = true
}


resource "aws_mq_broker" "example" {
  broker_name = "example"
  engine_type        = "ActiveMQ"
  engine_version     = "5.15.9"
  host_instance_type = "mq.m5.large"
  security_groups = [data.aws_security_group.selected.id]
  deployment_mode = "ACTIVE_STANDBY_MULTI_AZ"

  user {
    username = "ExampleUser"
    password = "MindTheGap-MindTheGap"
  }
}