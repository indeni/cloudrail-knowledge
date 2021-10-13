from cloudrail.knowledge.rules.aws.non_context_aware.ensure_rest_api_method_use_authentication_rule import EnsureRestApiMethodUseAuthenticationRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureRestApiMethodUseAuthenticationRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRestApiMethodUseAuthenticationRule()

    def test_method_with_authorization(self):
        self.run_test_case('method_with_authorization', False)

    def test_method_with_no_authorization(self):
        self.run_test_case('method_with_no_authorization', True)
