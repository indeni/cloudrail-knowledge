
resource "aws_mq_broker" "example" {
  broker_name = "example"
  engine_type        = "ActiveMQ"
  engine_version     = "5.15.9"
  storage_type       = "efs"
  host_instance_type = "mq.m5.large"
  deployment_mode = "ACTIVE_STANDBY_MULTI_AZ"

  user {
    username = "ExampleUser"
    password = "MindTheGap-MindTheGap"
  }
}