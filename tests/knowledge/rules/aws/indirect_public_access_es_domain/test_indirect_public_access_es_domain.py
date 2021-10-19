from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_elastic_search_rule import \
    IndirectPublicAccessElasticSearchRule

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestIndirectPublicAccessElasticSearchDomain(AwsBaseRuleTest):

    def get_rule(self):
        return IndirectPublicAccessElasticSearchRule()

    @rule_test('public_ec2_points_to_private_domain', True)
    def test_public_ec2_points_to_private_domain(self, rule_result: RuleResponse):
        pass

    @rule_test('private_ec2_points_to_private_domain', False)
    def test_private_ec2_points_to_private_domain(self, rule_result: RuleResponse):
        pass
