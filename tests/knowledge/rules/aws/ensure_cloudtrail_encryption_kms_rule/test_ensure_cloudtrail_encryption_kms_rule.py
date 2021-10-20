from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_cloudtrail_encryption_kms_rule import \
    EnsureCloudTrailEncryptionKmsRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureCloudTrailEncryptionKmsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudTrailEncryptionKmsRule()

    @rule_test('encrypted', False)
    def test_encrypted(self, rule_result: RuleResponse):
        pass

    @rule_test('non_encrypted', True)
    def test_non_encrypted(self, rule_result: RuleResponse):
        pass
