from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_elasticsearch_rule import PublicAccessElasticSearchRule


class TestPublicAccessElasticSearchRule(AwsBaseRuleTest):

    def get_rule(self):
        return PublicAccessElasticSearchRule()

    @rule_test('public-es', True)
    def test_public_es(self, rule_result: RuleResponse):
        pass

    @rule_test('vpc-controlled-private-es', False)
    def test_vpc_controlled_private_es(self, rule_result: RuleResponse):
        pass
