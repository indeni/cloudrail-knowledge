data "aws_caller_identity" "current" {}

resource "aws_sns_topic" "aws_sns_topic" {
  name = "glacier-sns-topic"
}

resource "aws_glacier_vault" "not_secure_archive" {
  name = "not_secure_archive"
  tags = {
    Name = "Glacier Cloudrail Test"
  }

  notification {
    sns_topic = aws_sns_topic.aws_sns_topic.arn
    events    = ["ArchiveRetrievalCompleted", "InventoryRetrievalCompleted"]
  }

  access_policy = <<EOF
{
    "Version":"2012-10-17",
    "Statement":[
       {
          "Sid": "add-read-only-perm",
          "Principal": "*",
          "Effect": "Allow",
          "Action": [
             "glacier:*"
          ],
          "Resource": "arn:aws:glacier:us-east-1:${data.aws_caller_identity.current.account_id}:vaults/not_secure_archive"
       }
    ]
}
EOF
}