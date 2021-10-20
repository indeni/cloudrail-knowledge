from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudwatch_log_groups_specify_retention_days_rule import \
    EnsureCloudWatchLogGroupsRetentionUsageRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureCloudWatchLogGroupsRetentionUsageRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudWatchLogGroupsRetentionUsageRule()

    @rule_test('no_retantion', True)
    def test_no_retantion(self, rule_result: RuleResponse):
        pass

    @rule_test('retention_configured', False)
    def test_retention_configured(self, rule_result: RuleResponse):
        pass
