from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_neptune_rule import PublicAccessDbNeptuneRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestPublicAccessDbNeptuneRule(AwsBaseRuleTest):

    def get_rule(self):
        return PublicAccessDbNeptuneRule()

    @rule_test('vpc_non_default', False)
    def test_vpc_non_default(self, rule_result: RuleResponse):
        pass

    @rule_test('external_vpc_with_igw', True, 2)
    def test_external_vpc_with_igw(self, rule_result: RuleResponse):
        pass
