provider "aws" {
  region = "us-east-1"
}

resource "aws_efs_file_system" "cloudrail" {
  creation_token = "cloudrail-encrypted"
  encrypted      = true

  tags = {
    Name = "Encrypted"
  }
}
