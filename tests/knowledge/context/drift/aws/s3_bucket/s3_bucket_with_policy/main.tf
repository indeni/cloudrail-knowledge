resource "aws_s3_bucket" "cloudrail-drift-test" {
  acl = "private"
}

resource "aws_s3_bucket_policy" "cloudrail-drift-test" {
  bucket = aws_s3_bucket.cloudrail-drift-test.id
  policy = <<-POLICY
    {
        "Version": "2012-10-17",
        "Id": "MyBucketPolicy",
        "Statement": [
            {
                "Sid": "AllowRead",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "${aws_s3_bucket.cloudrail-drift-test.arn}/*"
            }
        ]
    }
    POLICY
}

