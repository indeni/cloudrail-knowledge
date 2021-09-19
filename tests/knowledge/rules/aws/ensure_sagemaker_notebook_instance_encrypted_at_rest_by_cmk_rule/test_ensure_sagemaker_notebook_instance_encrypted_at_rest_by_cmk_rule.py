from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sagemaker_notebook_instance_encrypted_by_cmk import \
    EnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule()

    def test_sagemaker_notebook_instance_encrypted_cmk(self):
        self.run_test_case('sagemaker_notebook_instance_encrypted_cmk', False)

    def test_sagemaker_notebook_instance_encrypted_aws(self):
        self.run_test_case('sagemaker_notebook_instance_encrypted_aws', True)
