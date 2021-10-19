from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.disallow_ec2_classic_mode_rule import DisallowEc2ClassicModeRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class DisallowEc2ClassicModeRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return DisallowEc2ClassicModeRule()

    @rule_test('deploy_redshift_in_ec2_vpc_mode', False)
    def test_deploy_redshift_in_ec2_vpc_mode(self, rule_result: RuleResponse):
        pass

    @rule_test('deploy_redshift_in_ec2_classic_mode', True)
    def test_deploy_redshift_in_ec2_classic_mode(self, rule_result: RuleResponse):
        pass
