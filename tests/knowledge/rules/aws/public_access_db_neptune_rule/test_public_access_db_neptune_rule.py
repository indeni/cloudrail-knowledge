from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_neptune_rule import PublicAccessDbNeptuneRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestPublicAccessDbNeptuneRule(AwsBaseRuleTest):

    def get_rule(self):
        return PublicAccessDbNeptuneRule()

    def test_vpc_non_default(self):
        self.run_test_case('vpc_non_default', False)

    def test_external_vpc_with_igw(self):
        self.run_test_case('external_vpc_with_igw', True, 2)
