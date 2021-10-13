from cloudrail.knowledge.rules.aws.non_context_aware.allow_only_private_amis_rule import AllowOnlyPrivateAmisRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestAllowOnlyPrivateAmisRule(AwsBaseRuleTest):

    def get_rule(self):
        return AllowOnlyPrivateAmisRule()

    def test_ec2_3private_1public_image(self):
        self.run_test_case('ec2_3private_1public_image', True)

    def test_ec2_private_images_only(self):
        self.run_test_case('ec2_private_images_only', False)
