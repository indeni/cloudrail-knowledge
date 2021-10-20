
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

resource "aws_kms_key" "cw-log-group" {
  description             = "KMS key for Cloudwath Log Group"
  deletion_window_in_days = 7
  policy                  = <<POLICY
{
    "Version": "2012-10-17",
    "Id": "Key Policy",
    "Statement": [
        {
            "Sid": "Enable IAM User Permissions",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
                ]
            },
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Sid": "Allow Cloudwath Logs",
            "Effect": "Allow",
            "Principal": {
                "Service": "logs.${data.aws_region.current.name}.amazonaws.com"
            },
            "Action": [
                "kms:Encrypt*",
                "kms:Decrypt*",
                "kms:ReEncrypt*",
                "kms:GenerateDataKey*",
                "kms:Describe*"
            ],
            "Resource": "*"
        }
    ]
}
POLICY
}

resource "aws_cloudwatch_log_group" "cloudrail-test" {
  retention_in_days = 1
  kms_key_id        = aws_kms_key.cw-log-group.arn
}
