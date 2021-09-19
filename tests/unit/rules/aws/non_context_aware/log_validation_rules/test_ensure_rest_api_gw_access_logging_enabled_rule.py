import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_stage import AccessLogsSettings, ApiGatewayStage
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_rest_api_gw_access_logging_enabled_rule import \
    EnsureRestApiGwAccessLoggingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureRestApiGwAccessLoggingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRestApiGwAccessLoggingEnabledRule()

    def test_non_car_rest_api_gateway_access_logging_enabled_fail(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        rest_api_stage: ApiGatewayStage = create_empty_entity(ApiGatewayStage)
        rest_api_gw.api_gw_stages = [rest_api_stage]
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw], rest_api_stages=[rest_api_stage])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rest_api_gateway_access_logging_enabled__logs_enabled__pass(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        rest_api_stage: ApiGatewayStage = create_empty_entity(ApiGatewayStage)
        stage_access_logs: AccessLogsSettings = create_empty_entity(AccessLogsSettings)
        stage_access_logs.destination_arn = 'some_arn'
        stage_access_logs.format = 'some_format'
        rest_api_stage.access_logs = stage_access_logs
        rest_api_gw.api_gw_stages = [rest_api_stage]
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw], rest_api_stages=[rest_api_stage])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rest_api_gateway_access_logging_enabled__no_stage__pass(self):
        # Arrange
        rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
        rest_api_stage: ApiGatewayStage = create_empty_entity(ApiGatewayStage)
        stage_access_logs: AccessLogsSettings = create_empty_entity(AccessLogsSettings)
        stage_access_logs.destination_arn = 'some_arn'
        stage_access_logs.format = 'some_format'
        rest_api_stage.access_logs = stage_access_logs
        rest_api_gw.api_gw_stages = []
        context = AwsEnvironmentContext(rest_api_gw=[rest_api_gw], rest_api_stages=[rest_api_stage])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
