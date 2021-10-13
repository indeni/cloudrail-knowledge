

resource "aws_kms_key" "codebuild" {
  description             = "KMS key for Codebuild project"
  deletion_window_in_days = 7
}

# No policy attached to this role because it is for testing purposes
resource "aws_iam_role" "codebuild" {
  name = "codebuild-cloudrail-test"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_codebuild_project" "project-cloudrail-test" {
  name           = "project-cloudrail-test"
  description    = "project-cloudrail-test"
  build_timeout  = "5"
  queued_timeout = "5"
  service_role   = aws_iam_role.codebuild.arn
  encryption_key = aws_kms_key.codebuild.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  cache {
    type  = "LOCAL"
    modes = ["LOCAL_DOCKER_LAYER_CACHE", "LOCAL_SOURCE_CACHE"]
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:1.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"

    environment_variable {
      name  = "SOME_KEY1"
      value = "SOME_VALUE1"
    }
  }

  source {
    type            = "GITHUB"
    location        = "https://github.com/mitchellh/packer.git"
    git_clone_depth = 1
  }
}