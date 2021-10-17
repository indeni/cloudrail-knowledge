
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

resource "aws_config_configuration_aggregator" "test" {
  name = "all_regions_disabled_organization"

  organization_aggregation_source {
    role_arn = aws_iam_role.organization.arn
    regions  = [data.aws_region.current.name]
  }
}

resource "aws_iam_role" "organization" {
  name = "example"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "config.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "organization" {
  role       = aws_iam_role.organization.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSConfigRoleForOrganizations"
}
