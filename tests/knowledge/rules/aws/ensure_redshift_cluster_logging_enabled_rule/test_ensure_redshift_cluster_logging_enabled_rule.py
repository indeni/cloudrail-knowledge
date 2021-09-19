from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_redshift_cluster_logging_enabled_rule import \
    EnsureRedshiftClusterLoggingEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureRedshiftClusterLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRedshiftClusterLoggingEnabledRule()

    def test_logging_enabled(self):
        self.run_test_case('logging_enabled', False)

    def test_logging_disabled(self):
        self.run_test_case('logging_disabled', True)
