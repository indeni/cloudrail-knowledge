from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_lambda_function_cannot_be_invoked_public_rule import \
    EnsureLambdaFunctionCannotBeInvokedPublicRule

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureLambdaFunctionCannotBeInvokedPublicRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLambdaFunctionCannotBeInvokedPublicRule()

    @rule_test('public_lambda', True)
    def test_public_lambda(self, rule_result: RuleResponse):
        pass

    @rule_test('non_public_lambda', False)
    def test_non_public_lambda(self, rule_result: RuleResponse):
        pass

    @rule_test('link_with_arn', False)
    def test_link_with_arn(self, rule_result: RuleResponse):
        pass

    @rule_test('link_with_function_name', False)
    def test_link_with_function_name(self, rule_result: RuleResponse):
        pass

    @rule_test('link_with_partial_arn', False)
    def test_link_with_partial_arn(self, rule_result: RuleResponse):
        pass

    @rule_test('link_with_using_qualifier', False)
    def test_link_with_using_qualifier(self, rule_result: RuleResponse):
        pass

    @rule_test('link_with_using_qualifier_public_lambda', True)
    def test_link_with_using_qualifier_public_lambda(self, rule_result: RuleResponse):
        pass
