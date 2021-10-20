from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_db_redshift_rule import \
    IndirectPublicAccessDbRedshift

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestIndirectPublicAccessDbRedshift(AwsBaseRuleTest):

    def get_rule(self):
        return IndirectPublicAccessDbRedshift()

    @rule_test('public_ec2_points_to_private_redshift', True)
    def test_public_ec2_points_to_private_redshift(self, rule_result: RuleResponse):
        pass

    @rule_test('private_ec2_points_to_private_redshift', False)
    def test_private_ec2_points_to_private_redshift(self, rule_result: RuleResponse):
        pass
