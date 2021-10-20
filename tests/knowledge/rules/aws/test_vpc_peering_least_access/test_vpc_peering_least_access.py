from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.vpc_peering_least_access_rule import VpcPeeringLeastAccessRule


class TestVpcPeeringLeastAccess(AwsBaseRuleTest):

    def get_rule(self):
        return VpcPeeringLeastAccessRule()

    @rule_test('routes_appropriately_restrictive', False)
    def test_routes_appropriately_restrictive(self, rule_result: RuleResponse):
        pass

    @rule_test('routes_too_permissive_matching_exactly_VPC', True)
    def test_routes_too_permissive_matching_exactly_VPC(self, rule_result: RuleResponse):
        pass

    @rule_test('routes_too_permissive_wider_than_VPC', True)
    def test_routes_too_permissive_wider_than_VPC(self, rule_result: RuleResponse):
        pass
