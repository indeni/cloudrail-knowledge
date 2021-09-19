import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_rest_api_method_use_authentication_rule import EnsureRestApiMethodUseAuthenticationRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureRestApiMethodUseAuthenticationRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRestApiMethodUseAuthenticationRule()

    def test_non_car_api_gateway_methods_use_authentication_fail(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        api_method: ApiGatewayMethod = create_empty_entity(ApiGatewayMethod)
        api_method.authorization = 'NONE'
        rest_api_gw.api_gateway_methods = [api_method]
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw], api_gateway_methods=[api_method])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_api_gateway_methods_use_authentication_pass(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        api_method: ApiGatewayMethod = create_empty_entity(ApiGatewayMethod)
        api_method.authorization = 'AWS_IAM'
        rest_api_gw.api_gateway_methods = [api_method]
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw], api_gateway_methods=[api_method])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
