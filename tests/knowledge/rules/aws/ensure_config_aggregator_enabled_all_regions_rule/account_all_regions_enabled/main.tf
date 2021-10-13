
data "aws_caller_identity" "current" {}

resource "aws_config_configuration_aggregator" "test" {
  name = "all_regions_enabled_account"

  account_aggregation_source {
    account_ids = [data.aws_caller_identity.current.account_id]
    all_regions = true
  }
}

