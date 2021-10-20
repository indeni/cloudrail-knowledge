from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_docdb_logging_enabled_rule import EnsureDocdbLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureDocdbLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDocdbLoggingEnabledRule()

    @rule_test('docdb_cluster_no_logs_exports', True)
    def test_docdb_cluster_no_logs_exports(self, rule_result: RuleResponse):
        pass

    @rule_test('docdb_cluster_with_logs_exports', False)
    def test_docdb_cluster_with_logs_exports(self, rule_result: RuleResponse):
        pass
