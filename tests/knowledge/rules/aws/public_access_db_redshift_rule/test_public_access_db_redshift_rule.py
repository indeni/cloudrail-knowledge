from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_redshift_rule import PublicAccessDbRedshiftRule


class PublicAccessDbRedshiftRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return PublicAccessDbRedshiftRule()

    @rule_test('redshift_with_public_access', True)
    def test_redshift_with_public_access(self, rule_result: RuleResponse):
        pass

    @rule_test('redshift_without_public_access', False)
    def test_redshift_without_public_access(self, rule_result: RuleResponse):
        pass
