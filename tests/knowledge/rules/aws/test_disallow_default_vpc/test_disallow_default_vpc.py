from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.disallow_resources_in_default_vpc_rule import DisallowResourcesInDefaultVpcRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestDisallowDefaultVpcRule(AwsBaseRuleTest):

    def get_rule(self):
        return DisallowResourcesInDefaultVpcRule()

    @rule_test('deploy_ec2_to_default_vpc', True)
    def test_deploy_ec2_to_default_vpc(self, rule_result: RuleResponse):
        pass

    @rule_test('deploy_ec2_to_specific_vpc', False)
    def test_deploy_ec2_to_specific_vpc(self, rule_result: RuleResponse):
        pass
