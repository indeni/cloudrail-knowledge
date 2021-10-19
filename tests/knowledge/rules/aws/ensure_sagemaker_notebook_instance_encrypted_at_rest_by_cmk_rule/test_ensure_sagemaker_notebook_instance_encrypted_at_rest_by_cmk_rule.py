from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sagemaker_notebook_instance_encrypted_by_cmk import \
    EnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule()

    @rule_test('sagemaker_notebook_instance_encrypted_cmk', False)
    def test_sagemaker_notebook_instance_encrypted_cmk(self, rule_result: RuleResponse):
        pass

    @rule_test('sagemaker_notebook_instance_encrypted_aws', True)
    def test_sagemaker_notebook_instance_encrypted_aws(self, rule_result: RuleResponse):
        pass
