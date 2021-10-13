from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_cloud_watch_log_groups_encrypted_rule import \
    EnsureCloudWatchLogGroupsEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureCloudWatchLogGroupsEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudWatchLogGroupsEncryptedRule()

    def test_encrypted(self):
        self.run_test_case('encrypted', False)

    def test_non_encrypted(self):
        self.run_test_case('non_encrypted', True)

    def test_encrypted_customer_key_alias(self):
        self.run_test_case('encrypted_customer_key_alias', False)
