from cloudrail.knowledge.rules.azure.non_context_aware.public_access_sql_database_rule import PublicAccessSqlDatabaseRule
from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestPublicAccessSqlDatabaseRule(AzureBaseRuleTest):
    def get_rule(self):
        return PublicAccessSqlDatabaseRule()

    def test_allow_public_access(self):
        self.run_test_case('allow_public_access',
                           should_alert=True)

    def test_deny_public_access(self):
        self.run_test_case('deny_public_access',
                           should_alert=False)
