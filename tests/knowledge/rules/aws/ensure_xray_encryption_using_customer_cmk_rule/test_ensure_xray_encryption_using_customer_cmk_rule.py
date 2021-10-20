from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_xray_encryption_using_customer_cmk_rule import \
    EnsureXrayEncryptionCmkRule


class TestEnsureXrayEncryptionCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureXrayEncryptionCmkRule()

    @rule_test('kms_key_arn_aws_managed', True)
    def test_kms_key_arn_aws_managed(self, rule_result: RuleResponse):
        pass

    @rule_test('no_kms_encryption', True)
    def test_no_kms_encryption(self, rule_result: RuleResponse):
        pass

    @rule_test('kms_key_customer_creating', False)
    def test_kms_key_customer_creating(self, rule_result: RuleResponse):
        pass

    @rule_test('kms_key_customer_existing', False)
    def test_kms_key_customer_existing(self, rule_result: RuleResponse):
        pass
