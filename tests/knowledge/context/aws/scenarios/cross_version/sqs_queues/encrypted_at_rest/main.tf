resource "aws_sqs_queue" "cloudrail" {

  name                      = "sqs_encrypted"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  kms_master_key_id = "alias/aws/sqs"
  tags = {
    Environment = "production"
  }
}


resource "aws_sqs_queue" "cloudrail_2" {

  name                      = "sqs_encrypted_2"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  kms_master_key_id = "alias/aws/sqs"
  tags = {
    Environment = "production"
  }
}
