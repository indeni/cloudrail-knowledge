
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

resource "aws_config_configuration_aggregator" "test" {
  name = "all_regions_disabled_organization"

  account_aggregation_source {
    account_ids = [data.aws_caller_identity.current.account_id]
    regions     = [data.aws_region.current.name]
  }
}
