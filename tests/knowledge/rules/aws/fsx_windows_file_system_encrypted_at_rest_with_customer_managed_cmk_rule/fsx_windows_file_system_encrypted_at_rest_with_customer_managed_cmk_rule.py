from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest \
    .fsx_windows_file_system_encrypted_at_rest_with_customer_managed_cmk_rule import \
    FsxWindowsFileSystemEncryptedAtRestWithCustomerManagedCmkRule

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEsEncryptNodeToNodeRule(AwsBaseRuleTest):

    def get_rule(self):
        return FsxWindowsFileSystemEncryptedAtRestWithCustomerManagedCmkRule()

    def test_encrypted_with_aws_managed_cmk_by_default(self):
        self.run_test_case('encrypted_with_aws_managed_cmk_by_default', True)

    def test_encrypted_with_aws_managed_cmk_by_key_arn(self):
        self.run_test_case('encrypted_with_aws_managed_cmk_by_key_arn', True)

    def test_encrypted_with_customer_managed_cmk_creating_key(self):
        self.run_test_case('encrypted_with_customer_managed_cmk_creating_key', False)
