from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_no_direct_internet_access_allowed_to_sagemaker_notebook_instance_rule import \
    EnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule()

    @rule_test('no_public_access_sagemaker', False)
    def test_no_public_access_sagemaker(self, rule_result: RuleResponse):
        pass

    @rule_test('sagemaker_notebook_instance_aws_managed_encrypted', True)
    def test_sagemaker_notebook_instance_aws_managed_encrypted(self, rule_result: RuleResponse):
        pass
