from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_neptune_cluster_logging_enabled_rule import \
    EnsureNeptuneClusterLoggingEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureNeptuneClusterLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNeptuneClusterLoggingEnabledRule()

    def test_logging_disabled(self):
        self.run_test_case('logging_disabled', True)

    def test_logging_enabled(self):
        self.run_test_case('logging_enabled', False)
