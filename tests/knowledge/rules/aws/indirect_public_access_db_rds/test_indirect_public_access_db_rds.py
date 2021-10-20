from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_db_rds_rule import \
    IndirectPublicAccessDbRds

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestIndirectPublicAccessDbRds(AwsBaseRuleTest):

    def get_rule(self):
        return IndirectPublicAccessDbRds()

    @rule_test('public_ec2_points_to_private_rds', True)
    def test_public_ec2_points_to_private_rds(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("RDS Instance `aws_db_instance.test` does not have public IP associated."
                        " RDS Instance is on subnets: `aws_subnet.nondefault_1" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'tf-test-db')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'RDS Instance')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_security_group.db')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    @rule_test('private_ec2_points_to_private_rds', False)
    def test_private_ec2_points_to_private_rds(self, rule_result: RuleResponse):
        pass
