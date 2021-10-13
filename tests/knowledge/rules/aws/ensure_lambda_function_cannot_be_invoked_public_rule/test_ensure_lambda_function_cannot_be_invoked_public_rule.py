from cloudrail.knowledge.rules.aws.non_context_aware.ensure_lambda_function_cannot_be_invoked_public_rule import \
    EnsureLambdaFunctionCannotBeInvokedPublicRule

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureLambdaFunctionCannotBeInvokedPublicRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLambdaFunctionCannotBeInvokedPublicRule()

    def test_public_lambda(self):
        self.run_test_case('public_lambda', True)

    def test_non_public_lambda(self):
        self.run_test_case('non_public_lambda', False)

    def test_link_with_arn(self):
        self.run_test_case('link_with_arn', False)

    def test_link_with_function_name(self):
        self.run_test_case('link_with_function_name', False)

    def test_link_with_partial_arn(self):
        self.run_test_case('link_with_partial_arn', False)

    def test_link_with_using_qualifier(self):
        self.run_test_case('link_with_using_qualifier', False)

    def test_link_with_using_qualifier_public_lambda(self):
        self.run_test_case('link_with_using_qualifier_public_lambda', True)
