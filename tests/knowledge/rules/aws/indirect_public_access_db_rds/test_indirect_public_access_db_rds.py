from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_db_rds_rule import \
    IndirectPublicAccessDbRds

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestIndirectPublicAccessDbRds(AwsBaseRuleTest):

    def get_rule(self):
        return IndirectPublicAccessDbRds()

    def test_public_ec2_points_to_private_rds(self):
        rule_result = self.run_test_case('public_ec2_points_to_private_rds', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("RDS Instance `aws_db_instance.test` does not have public IP associated."
                        " RDS Instance is on subnets: `aws_subnet.nondefault_1" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'tf-test-db')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'RDS Instance')
        self.assertEqual(rule_result.issues[0].violating.iac_state.resource_metadata.iac_entity_id, 'aws_security_group.db')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    def test_private_ec2_points_to_private_rds(self):
        self.run_test_case('private_ec2_points_to_private_rds', False)
