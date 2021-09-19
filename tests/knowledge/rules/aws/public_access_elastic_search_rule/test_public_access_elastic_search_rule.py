from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_elasticsearch_rule import PublicAccessElasticSearchRule


class TestPublicAccessElasticSearchRule(AwsBaseRuleTest):

    def get_rule(self):
        return PublicAccessElasticSearchRule()

    def test_public_es(self):
        self.run_test_case('public-es', True)

    def test_vpc_controlled_private_es(self):
        self.run_test_case('vpc-controlled-private-es', False)
