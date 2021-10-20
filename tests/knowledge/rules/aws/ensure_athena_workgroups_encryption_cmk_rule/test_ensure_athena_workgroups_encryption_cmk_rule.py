from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_workgroups_encryption_cmk_rule import \
    EnsureAthenaWorkgroupsEncryptionCmkRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureAthenaWorkgroupsEncryptionCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureAthenaWorkgroupsEncryptionCmkRule()

    @rule_test('encrypted_sse_kms_cmk', False)
    def test_encrypted_sse_kms_cmk(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_cse_kms_cmk', False)
    def test_encrypted_cse_kms_cmk(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_sse_kms_s3', True)
    def test_encrypted_sse_kms_s3(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_work_groups', True, 2)
    def test_encrypted_work_groups(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_sse_s3', True)
    def test_encrypted_sse_s3(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_cse_kms_alias_s3', True)
    def test_encrypted_cse_kms_alias_s3(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_sse_kms_existing_key_alias', False)
    def test_encrypted_sse_kms_existing_key_alias(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_sse_kms_alias_s3', True)
    def test_encrypted_sse_kms_alias_s3(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_cse_kms_existing_key_alias', False)
    def test_encrypted_cse_kms_existing_key_alias(self, rule_result: RuleResponse):
        pass
