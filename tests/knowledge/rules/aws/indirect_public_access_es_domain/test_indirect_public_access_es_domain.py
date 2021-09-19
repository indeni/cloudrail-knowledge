from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_elastic_search_rule import \
    IndirectPublicAccessElasticSearchRule

from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestIndirectPublicAccessElasticSearchDomain(AwsBaseRuleTest):

    def get_rule(self):
        return IndirectPublicAccessElasticSearchRule()

    def test_public_ec2_points_to_private_domain(self):
        self.run_test_case('public_ec2_points_to_private_domain', True)

    def test_private_ec2_points_to_private_domain(self):
        self.run_test_case('private_ec2_points_to_private_domain', False)
