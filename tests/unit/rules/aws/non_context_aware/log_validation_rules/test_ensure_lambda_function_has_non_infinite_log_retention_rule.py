import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_log_group import CloudWatchLogGroup
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_lambda_function_has_non_infinite_log_retention_rule import \
    EnsureLambdaFunctionHasNonInfiniteLogRetentionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureLambdaFunctionHasNonInfiniteLogRetentionRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureLambdaFunctionHasNonInfiniteLogRetentionRule()

    def test_non_car_lambda_logging_not_infinite_fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        lambda_func.log_group = log_group
        lambda_func.log_group.retention_in_days = 0
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func], cloud_watch_log_groups=[log_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_lambda_logging_not_infinite__no_retention__fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        lambda_func.log_group = log_group
        lambda_func.log_group.retention_in_days = None
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func], cloud_watch_log_groups=[log_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue('Upon creation' not in result.issues[0].evidence)

    def test_non_car_lambda_logging_not_infinite__no_retention_and_pseudo___fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        lambda_func.log_group = log_group
        lambda_func.log_group.retention_in_days = None
        lambda_func.log_group.is_pseudo = True
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue('Upon creation' in result.issues[0].evidence)

    def test_non_car_lambda_logging_not_infinite_pass(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        lambda_func.log_group = log_group
        lambda_func.log_group.retention_in_days = 10
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_lambda_logging_not_infinite__no_log_group(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
