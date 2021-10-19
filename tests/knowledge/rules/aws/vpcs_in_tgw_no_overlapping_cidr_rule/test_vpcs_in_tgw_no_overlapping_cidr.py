from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.vpcs_in_tgw_no_overlapping_cidr_rule import VpcsInTransitGatewayNoOverlappingCidrRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestVpcsInTransitGatewayNoOverlappingCidrRule(AwsBaseRuleTest):

    def get_rule(self):
        return VpcsInTransitGatewayNoOverlappingCidrRule()

    @rule_test('typical_setup_no_issue', False)
    def test_typical_setup_no_issue(self, rule_result: RuleResponse):
        pass

    @rule_test('overlapping_routes', True)
    def test_overlapping_routes(self, rule_result: RuleResponse):
        pass
