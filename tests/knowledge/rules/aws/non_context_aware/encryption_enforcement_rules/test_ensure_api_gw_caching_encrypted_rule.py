import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import ApiGatewayMethodSettings, RestApiMethod
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.ensure_api_gw_caching_encrypted_rule import \
    EnsureApiGwCachingEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureApiGwCachingEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureApiGwCachingEncryptedRule()

    def test_non_car_api_gateway_caching_encrypted_fail(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        method_settings: ApiGatewayMethodSettings = create_empty_entity(ApiGatewayMethodSettings)
        rest_api_gw.method_settings = method_settings
        rest_api_gw.method_settings.http_method = RestApiMethod.HEAD
        rest_api_gw.method_settings.stage_name = 'method_tests'
        rest_api_gw.method_settings.caching_enabled = True
        rest_api_gw.method_settings.caching_encrypted = False
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_api_gateway_caching_encrypted_pass(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        method_settings: ApiGatewayMethodSettings = create_empty_entity(ApiGatewayMethodSettings)
        rest_api_gw.method_settings = method_settings
        rest_api_gw.method_settings.http_method = RestApiMethod.HEAD
        rest_api_gw.method_settings.stage_name = 'method_tests'
        rest_api_gw.method_settings.caching_enabled = False
        rest_api_gw.method_settings.caching_encrypted = False
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_api_gateway_caching_encrypted__cache_encrypt__pass(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        method_settings: ApiGatewayMethodSettings = create_empty_entity(ApiGatewayMethodSettings)
        rest_api_gw.method_settings = method_settings
        rest_api_gw.method_settings.http_method = RestApiMethod.HEAD
        rest_api_gw.method_settings.stage_name = 'method_tests'
        rest_api_gw.method_settings.caching_enabled = True
        rest_api_gw.method_settings.caching_encrypted = True
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_api_gateway_caching_encrypted__no_methods__pass(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        rest_api_gw.method_settings = None
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
