import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_lambda_function_cannot_be_invoked_public_rule import \
    EnsureLambdaFunctionCannotBeInvokedPublicRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureLambdaFunctionCannotBeInvokedPublicRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureLambdaFunctionCannotBeInvokedPublicRule()

    def test_non_car_lambda_public_exposure_fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))])
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_lambda_public_exposure__denay_effect__pass(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.DENY,
                                                                               ['lambda:*'], ['*'],
                                                                               Principal(PrincipalType.AWS, ['*']))])
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_lambda_func_policy_wildcard__no_invoke_action__pass(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:GetLogs'], ['*'],
                                                                               Principal(PrincipalType.PUBLIC, ['*']))])
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
