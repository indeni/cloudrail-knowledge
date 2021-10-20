from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_cloud_watch_log_groups_encrypted_rule import \
    EnsureCloudWatchLogGroupsEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureCloudWatchLogGroupsEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudWatchLogGroupsEncryptedRule()

    @rule_test('encrypted', False)
    def test_encrypted(self, rule_result: RuleResponse):
        pass

    @rule_test('non_encrypted', True)
    def test_non_encrypted(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_customer_key_alias', False)
    def test_encrypted_customer_key_alias(self, rule_result: RuleResponse):
        pass
