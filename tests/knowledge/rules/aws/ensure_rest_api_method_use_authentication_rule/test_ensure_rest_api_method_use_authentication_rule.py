from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_rest_api_method_use_authentication_rule import EnsureRestApiMethodUseAuthenticationRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureRestApiMethodUseAuthenticationRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRestApiMethodUseAuthenticationRule()

    @rule_test('method_with_authorization', False)
    def test_method_with_authorization(self, rule_result: RuleResponse):
        pass

    @rule_test('method_with_no_authorization', True)
    def test_method_with_no_authorization(self, rule_result: RuleResponse):
        pass
