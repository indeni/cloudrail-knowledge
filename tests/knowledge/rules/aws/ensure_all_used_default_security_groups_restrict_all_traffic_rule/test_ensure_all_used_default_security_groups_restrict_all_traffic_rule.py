from cloudrail.knowledge.rules.aws.context_aware.ensure_all_used_default_security_groups_restrict_all_traffic_rule import \
    EnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest



class TestEnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule()

    def test_default_sg_in_new_vpc(self):
        self.run_test_case('default_sg_in_new_vpc', True)

    def test_decelerated_sg_in_new_vpc(self):
        self.run_test_case('decelerated_sg_in_new_vpc', False)

    def test_decelerated_sg_with_rules_in_new_vpc(self):
        self.run_test_case('decelerated_sg_with_rules_in_new_vpc', True)

    def test_default_sg_with_ec2_using_ni(self):
        self.run_test_case('default_sg_with_ec2_using_ni', True)

    def test_ec2_simple_deceleration(self):
        self.run_test_case('ec2_simple_deceleration', True)
