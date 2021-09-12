import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_domain import RestApiGwDomain
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_api_gw_use_modern_tls_rule import EnsureApiGwUseModernTlsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureApiGwUseModernTlsRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureApiGwUseModernTlsRule()

    def test_non_car_api_gateway_tls_fail(self):
        # Arrange
        rest_api: RestApiGw = create_empty_entity(RestApiGw)
        rest_api_domain: RestApiGwDomain = create_empty_entity(RestApiGwDomain)
        rest_api_domain.security_policy = 'TLS_1.1'
        rest_api.domain = rest_api_domain
        context = AwsEnvironmentContext(rest_api_gw=[rest_api])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_api_gateway_tls_pass(self):
        # Arrange
        rest_api: RestApiGw = create_empty_entity(RestApiGw)
        rest_api_domain: RestApiGwDomain = create_empty_entity(RestApiGwDomain)
        rest_api_domain.security_policy = 'TLS_1.2'
        rest_api.domain = rest_api_domain
        context = AwsEnvironmentContext(rest_api_gw=[rest_api])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_api_gateway_tls__no_domain__pass(self):
        # Arrange
        rest_api: RestApiGw = create_empty_entity(RestApiGw)
        context = AwsEnvironmentContext(rest_api_gw=[rest_api])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
