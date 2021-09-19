from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules\
    .encrypt_at_rest.ensure_workspace_root_volume_encrypted_with_customer_cmk_rule \
    import EnsureWorkspaceRootVolumeEncryptionCmkRule


class TestEnsureWorkspaceRootVolumeEncryptionCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureWorkspaceRootVolumeEncryptionCmkRule()

    def test_aws_cmk_root_volume_encryption(self):
        self.run_test_case('aws_cmk_root_volume_encryption', True)

    def test_customer_cmk_root_volume_created(self):
        self.run_test_case('customer_cmk_root_volume_created', False)

    def test_customer_cmk_root_volume_existing(self):
        self.run_test_case('customer_cmk_root_volume_existing', False)
