from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudwatch_log_groups_specify_retention_days_rule import \
    EnsureCloudWatchLogGroupsRetentionUsageRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureCloudWatchLogGroupsRetentionUsageRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudWatchLogGroupsRetentionUsageRule()

    def test_no_retantion(self):
        self.run_test_case('no_retantion', True)

    def test_retention_configured(self):
        self.run_test_case('retention_configured', False)
