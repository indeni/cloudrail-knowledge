from cloudrail.knowledge.rules.aws.context_aware.vpcs_in_tgw_no_overlapping_cidr_rule import VpcsInTransitGatewayNoOverlappingCidrRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestVpcsInTransitGatewayNoOverlappingCidrRule(AwsBaseRuleTest):

    def get_rule(self):
        return VpcsInTransitGatewayNoOverlappingCidrRule()

    def test_typical_setup_no_issue(self):
        self.run_test_case('typical_setup_no_issue', False)

    def test_overlapping_routes(self):
        self.run_test_case('overlapping_routes', True)
