import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_stage import ApiGatewayStage
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_api_gw_xray_tracing_enabled_rule import \
    EnsureApiGwXrayTracingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureApiGwXrayTracingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureApiGwXrayTracingEnabledRule()

    def test_non_car_api_gateway_xray_tracing_enabled_fail(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        rest_api_stage: ApiGatewayStage = create_empty_entity(ApiGatewayStage)
        rest_api_stage.xray_tracing_enabled = False
        rest_api_gw.api_gw_stages = [rest_api_stage]
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw], rest_api_stages=[rest_api_stage])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_api_gateway_xray_tracing_enabled__tracing_enabled__pass(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        rest_api_stage: ApiGatewayStage = create_empty_entity(ApiGatewayStage)
        rest_api_stage.xray_tracing_enabled = True
        rest_api_gw.api_gw_stages = [rest_api_stage]
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw], rest_api_stages=[rest_api_stage])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_api_gateway_xray_tracing_enabled__no_stage__pass(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        rest_api_stage: ApiGatewayStage = create_empty_entity(ApiGatewayStage)
        rest_api_stage.xray_tracing_enabled = True
        rest_api_gw.api_gw_stages = []
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw], rest_api_stages=[rest_api_stage])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
