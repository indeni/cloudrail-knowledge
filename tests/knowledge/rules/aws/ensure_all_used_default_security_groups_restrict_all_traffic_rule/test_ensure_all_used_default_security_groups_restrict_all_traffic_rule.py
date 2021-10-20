from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.ensure_all_used_default_security_groups_restrict_all_traffic_rule import \
    EnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test



class TestEnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule()

    @rule_test('default_sg_in_new_vpc', True)
    def test_default_sg_in_new_vpc(self, rule_result: RuleResponse):
        pass

    @rule_test('decelerated_sg_in_new_vpc', False)
    def test_decelerated_sg_in_new_vpc(self, rule_result: RuleResponse):
        pass

    @rule_test('decelerated_sg_with_rules_in_new_vpc', True)
    def test_decelerated_sg_with_rules_in_new_vpc(self, rule_result: RuleResponse):
        pass

    @rule_test('default_sg_with_ec2_using_ni', True)
    def test_default_sg_with_ec2_using_ni(self, rule_result: RuleResponse):
        pass

    @rule_test('ec2_simple_deceleration', True)
    def test_ec2_simple_deceleration(self, rule_result: RuleResponse):
        pass
