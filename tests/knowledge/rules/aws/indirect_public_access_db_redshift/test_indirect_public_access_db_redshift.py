from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_db_redshift_rule import \
    IndirectPublicAccessDbRedshift

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestIndirectPublicAccessDbRedshift(AwsBaseRuleTest):

    def get_rule(self):
        return IndirectPublicAccessDbRedshift()

    def test_public_ec2_points_to_private_redshift(self):
        self.run_test_case('public_ec2_points_to_private_redshift', True)

    def test_private_ec2_points_to_private_redshift(self):
        self.run_test_case('private_ec2_points_to_private_redshift', False)
