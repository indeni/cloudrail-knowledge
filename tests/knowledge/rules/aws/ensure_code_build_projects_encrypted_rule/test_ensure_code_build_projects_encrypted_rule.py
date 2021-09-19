from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_code_build_projects_encrypted_rule import \
    EnsureCodeBuildProjectsEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest



class TestEnsureCodeBuildProjectsEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCodeBuildProjectsEncryptedRule()

    def test_default_encryption(self):
        self.run_test_case('default_encryption', True)

    def test_encrypted_aws_key_arn(self):
        self.run_test_case('encrypted_aws_key_arn', True)

    def test_encrypted_existing_customer_key(self):
        self.run_test_case('encrypted_existing_customer_key', False)

    def test_encrypted_new_customer_key(self):
        self.run_test_case('encrypted_new_customer_key', False)
