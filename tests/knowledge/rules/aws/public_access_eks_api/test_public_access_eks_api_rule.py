from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_eks_api_rule import PublicAccessEksApiRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class PublicAccessEksApiRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return PublicAccessEksApiRule()

    def test_eks_with_private_api(self):
        tf_use_case_folder_name = 'eks_with_private_api'
        self.run_test_case(tf_use_case_folder_name, False)

    def test_eks_with_public_api(self):
        tf_use_case_folder_name = 'eks_with_public_api'
        self.run_test_case(tf_use_case_folder_name, True)
