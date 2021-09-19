from cloudrail.knowledge.rules.aws.context_aware.disallow_resources_in_default_vpc_rule import DisallowResourcesInDefaultVpcRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestDisallowDefaultVpcRule(AwsBaseRuleTest):

    def get_rule(self):
        return DisallowResourcesInDefaultVpcRule()

    def test_deploy_ec2_to_default_vpc(self):
        self.run_test_case('deploy_ec2_to_default_vpc', True)

    def test_deploy_ec2_to_specific_vpc(self):
        self.run_test_case('deploy_ec2_to_specific_vpc', False)
