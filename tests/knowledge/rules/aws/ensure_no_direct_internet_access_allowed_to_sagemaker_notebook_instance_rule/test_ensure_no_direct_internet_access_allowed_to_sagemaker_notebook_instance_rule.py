from cloudrail.knowledge.rules.aws.non_context_aware.ensure_no_direct_internet_access_allowed_to_sagemaker_notebook_instance_rule import \
    EnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule()

    def test_no_public_access_sagemaker(self):
        self.run_test_case('no_public_access_sagemaker', False)

    def test_sagemaker_notebook_instance_aws_managed_encrypted(self):
        self.run_test_case('sagemaker_notebook_instance_aws_managed_encrypted', True)
