from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.ec2_role_share_rule import Ec2RoleShareRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class Ec2RoleShareRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return Ec2RoleShareRule()

    @rule_test('public_and_private_ec2_same_role', True)
    def test_public_and_private_ec2_same_role(self, rule_result: RuleResponse):
        pass

    @rule_test('public_and_private_ec2_different_role', False)
    def test_public_and_private_ec2_different_role(self, rule_result: RuleResponse):
        pass

    @rule_test('public_and_public_ec2_same_role', False)
    def test_public_and_public_ec2_same_role(self, rule_result: RuleResponse):
        pass

    @rule_test('private_and_private_ec2_same_role', False)
    def test_private_and_private_ec2_same_role(self, rule_result: RuleResponse):
        pass
