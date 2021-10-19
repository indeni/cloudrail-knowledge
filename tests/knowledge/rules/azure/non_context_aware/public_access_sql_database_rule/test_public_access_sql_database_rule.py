from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.public_access_sql_database_rule import PublicAccessSqlDatabaseRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestPublicAccessSqlDatabaseRule(AzureBaseRuleTest):
    def get_rule(self):
        return PublicAccessSqlDatabaseRule()

    @rule_test('allow_public_access', should_alert=True)
    def test_allow_public_access(self, rule_result: RuleResponse):
        pass

    @rule_test('deny_public_access', should_alert=False)
    def test_deny_public_access(self, rule_result: RuleResponse):
        pass
