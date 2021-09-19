
resource "aws_mq_broker" "example" {
  broker_name = "example"
  engine_type        = "ActiveMQ"
  engine_version     = "5.15.9"
  storage_type       = "ebs"
  host_instance_type = "mq.m5.large"

  user {
    username = "ExampleUser"
    password = "MindTheGap-MindTheGap"
  }
}