from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_code_build_projects_encrypted_rule import \
    EnsureCodeBuildProjectsEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test



class TestEnsureCodeBuildProjectsEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCodeBuildProjectsEncryptedRule()

    @rule_test('default_encryption', True)
    def test_default_encryption(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_aws_key_arn', True)
    def test_encrypted_aws_key_arn(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_existing_customer_key', False)
    def test_encrypted_existing_customer_key(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_new_customer_key', False)
    def test_encrypted_new_customer_key(self, rule_result: RuleResponse):
        pass
