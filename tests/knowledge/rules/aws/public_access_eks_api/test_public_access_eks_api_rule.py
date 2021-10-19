from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_eks_api_rule import PublicAccessEksApiRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class PublicAccessEksApiRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return PublicAccessEksApiRule()

    @rule_test('eks_with_private_api', False)
    def test_eks_with_private_api(self, rule_result: RuleResponse):
        pass

    @rule_test('eks_with_public_api', True)
    def test_eks_with_public_api(self, rule_result: RuleResponse):
        pass
