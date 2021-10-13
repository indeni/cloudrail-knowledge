from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_docdb_logging_enabled_rule import EnsureDocdbLoggingEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureDocdbLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDocdbLoggingEnabledRule()

    def test_docdb_cluster_no_logs_exports(self):
        self.run_test_case('docdb_cluster_no_logs_exports', True)

    def test_docdb_cluster_with_logs_exports(self):
        self.run_test_case('docdb_cluster_with_logs_exports', False)
