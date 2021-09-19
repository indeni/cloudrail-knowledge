from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_sql_server_audit_enabled_rule import EnsureSqlServerAuditEnabledRule


class TestEnsureSqlServerAuditEnabledRule(AzureBaseRuleTest):

    def get_rule(self):
        return EnsureSqlServerAuditEnabledRule()

    def test_audit_enabled_extended_block(self):
        self.run_test_case('audit_enabled_extended_block', False)

    def test_audit_enabled_extended_block_default_retention(self):
        self.run_test_case('audit_enabled_extended_block_default_retention', False)

    def test_audit_enabled_extended_block_retention_90(self):
        rule_result = self.run_test_case('audit_enabled_extended_block_retention_90', True)
        self.assertTrue('has auditing enabled, but for less than 90 days of retention' in rule_result.issues[0].evidence)

    def test_audit_enabled_server_extended_resource_default_retention(self):
        self.run_test_case('audit_enabled_server_extended_resource_default_retention', False)

    def test_audit_enabled_server_extended_resource_retention_90(self):
        rule_result = self.run_test_case('audit_enabled_server_extended_resource_retention_90', True)
        self.assertTrue('has auditing enabled, but for less than 90 days of retention' in rule_result.issues[0].evidence)

    def test_audit_not_enabled(self):
        rule_result = self.run_test_case('audit_not_enabled', True)
        self.assertTrue('does not have auditing enabled' in rule_result.issues[0].evidence)
