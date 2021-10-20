
resource "aws_vpc" "nondefault" {
  cidr_block = "10.1.1.0/24"
}

resource "aws_subnet" "nondefault_1" {
  vpc_id = aws_vpc.nondefault.id
  cidr_block = "10.1.1.128/25"
  availability_zone = "us-east-1c"
}

resource "aws_subnet" "nondefault_2" {
  vpc_id = aws_vpc.nondefault.id
  cidr_block = "10.1.1.0/25"
  availability_zone = "us-east-1d"
}

data "aws_workspaces_bundle" "value_windows_10" {
  bundle_id = "wsb-bh8rsxt14"
}

data "aws_iam_policy_document" "workspaces" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["workspaces.amazonaws.com"]
    }
  }
}

data "aws_kms_key" "by_alias" {
  key_id = "alias/aws/workspaces"
}

resource "aws_directory_service_directory" "test" {
  name     = "corp.notexample.com"
  password = "SuperSecretPassw0rd"
  size     = "Small"

  vpc_settings {
    vpc_id = aws_vpc.nondefault.id

    subnet_ids = [
      aws_subnet.nondefault_1.id,
      aws_subnet.nondefault_2.id
    ]
  }
}

resource "aws_workspaces_directory" "test" {
  directory_id = aws_directory_service_directory.test.id

  subnet_ids = [
    aws_subnet.nondefault_1.id,
    aws_subnet.nondefault_2.id
  ]

  depends_on = [
    aws_iam_role_policy_attachment.workspaces_default_service_access,
    aws_iam_role_policy_attachment.workspaces_default_self_service_access
  ]
}

resource "aws_iam_role" "workspaces_default" {
  name               = "workspaces_DefaultRole"
  assume_role_policy = data.aws_iam_policy_document.workspaces.json
}

resource "aws_iam_role_policy_attachment" "workspaces_default_service_access" {
  role       = aws_iam_role.workspaces_default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonWorkSpacesServiceAccess"
}

resource "aws_iam_role_policy_attachment" "workspaces_default_self_service_access" {
  role       = aws_iam_role.workspaces_default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonWorkSpacesSelfServiceAccess"
}

resource "aws_workspaces_workspace" "test" {
  directory_id = aws_workspaces_directory.test.id
  bundle_id    = data.aws_workspaces_bundle.value_windows_10.id
  user_name    = "Administrator"

  user_volume_encryption_enabled = true
  volume_encryption_key          = data.aws_kms_key.by_alias.arn

  workspace_properties {
    compute_type_name                         = "VALUE"
    user_volume_size_gib                      = 10
    root_volume_size_gib                      = 80
    running_mode                              = "AUTO_STOP"
    running_mode_auto_stop_timeout_in_minutes = 60
  }
}
