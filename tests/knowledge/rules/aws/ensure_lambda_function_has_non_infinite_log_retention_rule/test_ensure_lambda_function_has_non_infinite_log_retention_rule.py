from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_lambda_function_has_non_infinite_log_retention_rule import \
    EnsureLambdaFunctionHasNonInfiniteLogRetentionRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureLambdaFunctionHasNonInfiniteLogRetentionRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLambdaFunctionHasNonInfiniteLogRetentionRule()

    def test_lambda_with_infinite_retention(self):
        rule_result = self.run_test_case('lambda_with_infinite_retention', True)
        self.assertIsNotNone(rule_result)
        self.assertEqual('The CloudWatch Logs Group `aws_cloudwatch_log_group.log_group` has retention set to Never Expire',
                         rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Lambda Function')
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'cloudrail_test_lambda')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Group')
        self.assertEqual(rule_result.issues[0].violating.get_name(), '/aws/lambda/cloudrail_test_lambda')

    def test_lambda_with_log_retention_set(self):
        self.run_test_case('lambda_with_log_retention_set', False)

    def test_lambda_with_pseudo_log_group(self):
        rule_result = self.run_test_case('lambda_with_pseudo_log_group', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('Upon creation, Lambda Function `aws_lambda_function.test_lambda` will have a log group' in
                        rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Lambda Function')
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'cloudrail_test_lambda')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Lambda Function')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'cloudrail_test_lambda')

    def test_multiple_lambda_pdesudo_log_groups(self):
        rule_result = self.run_test_case('multiple_lambda_pdesudo_log_groups', True, 2)
        self.assertIsNotNone(rule_result)
        for item in rule_result.issues:
            self.assertTrue('Upon creation, Lambda Function' in item.evidence)
            self.assertEqual(item.exposed.get_type(), 'Lambda Function')
            self.assertEqual(item.violating.get_type(), 'Lambda Function')
        lambda_1 = next((item for item in rule_result.issues if item.exposed.get_name() == 'cloudrail_test_lambda'), None)
        lambda_2 = next((item for item in rule_result.issues if item.exposed.get_name() == 'cloudrail_test_lambda_2'), None)
        self.assertIsNotNone(lambda_1)
        self.assertIsNotNone(lambda_2)
