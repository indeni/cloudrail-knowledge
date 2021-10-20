from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules\
    .encrypt_at_rest.ensure_workspace_root_volume_encrypted_with_customer_cmk_rule \
    import EnsureWorkspaceRootVolumeEncryptionCmkRule


class TestEnsureWorkspaceRootVolumeEncryptionCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureWorkspaceRootVolumeEncryptionCmkRule()

    @rule_test('aws_cmk_root_volume_encryption', True)
    def test_aws_cmk_root_volume_encryption(self, rule_result: RuleResponse):
        pass

    @rule_test('customer_cmk_root_volume_created', False)
    def test_customer_cmk_root_volume_created(self, rule_result: RuleResponse):
        pass

    @rule_test('customer_cmk_root_volume_existing', False)
    def test_customer_cmk_root_volume_existing(self, rule_result: RuleResponse):
        pass
