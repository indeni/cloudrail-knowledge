from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_sql_server_audit_enabled_rule import EnsureSqlServerAuditEnabledRule


class TestEnsureSqlServerAuditEnabledRule(AzureBaseRuleTest):

    def get_rule(self):
        return EnsureSqlServerAuditEnabledRule()

    @rule_test('audit_enabled_extended_block', False)
    def test_audit_enabled_extended_block(self, rule_result: RuleResponse):
        pass

    @rule_test('audit_enabled_extended_block_default_retention', False)
    def test_audit_enabled_extended_block_default_retention(self, rule_result: RuleResponse):
        pass

    @rule_test('audit_enabled_extended_block_retention_90', True)
    def test_audit_enabled_extended_block_retention_90(self, rule_result: RuleResponse):
        self.assertTrue('has auditing enabled, but for less than 90 days of retention' in rule_result.issues[0].evidence)

    @rule_test('audit_enabled_server_extended_resource_default_retention', False)
    def test_audit_enabled_server_extended_resource_default_retention(self, rule_result: RuleResponse):
        pass

    @rule_test('audit_enabled_server_extended_resource_retention_90', True)
    def test_audit_enabled_server_extended_resource_retention_90(self, rule_result: RuleResponse):
        self.assertTrue('has auditing enabled, but for less than 90 days of retention' in rule_result.issues[0].evidence)

    @rule_test('audit_not_enabled', True)
    def test_audit_not_enabled(self, rule_result: RuleResponse):
        self.assertTrue('does not have auditing enabled' in rule_result.issues[0].evidence)
