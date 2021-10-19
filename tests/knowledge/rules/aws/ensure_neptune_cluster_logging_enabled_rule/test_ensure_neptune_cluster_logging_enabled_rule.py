from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_neptune_cluster_logging_enabled_rule import \
    EnsureNeptuneClusterLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureNeptuneClusterLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNeptuneClusterLoggingEnabledRule()

    @rule_test('logging_disabled', True)
    def test_logging_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('logging_enabled', False)
    def test_logging_enabled(self, rule_result: RuleResponse):
        pass
