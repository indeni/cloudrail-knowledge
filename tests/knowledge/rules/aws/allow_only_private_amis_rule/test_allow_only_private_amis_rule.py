from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.allow_only_private_amis_rule import AllowOnlyPrivateAmisRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestAllowOnlyPrivateAmisRule(AwsBaseRuleTest):

    def get_rule(self):
        return AllowOnlyPrivateAmisRule()

    @rule_test('ec2_3private_1public_image', True)
    def test_ec2_3private_1public_image(self, rule_result: RuleResponse):
        pass

    @rule_test('ec2_private_images_only', False)
    def test_ec2_private_images_only(self, rule_result: RuleResponse):
        pass
