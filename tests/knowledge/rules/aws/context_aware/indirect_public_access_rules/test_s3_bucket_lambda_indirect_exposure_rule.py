import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import ApiGatewayIntegration
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket

from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.s3_bucket_lambda_indirect_exposure_rule import \
    S3BucketLambdaIndirectExposureRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestS3BucketLambdaIndirectExposureRule(unittest.TestCase):
    def setUp(self):
        self.rule = S3BucketLambdaIndirectExposureRule()

    def test_s3_lambda_indirect_exposure_fail(self):
        # Arrange
        context = self._create_env(True, True)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_s3_lambda_indirect_exposure_pass1(self):
        # Arrange
        context = self._create_env(True, False)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_s3_lambda_indirect_exposure_pass2(self):
        # Arrange
        ctx = self._create_env(False, True)
        # Act
        result = self.rule.run(ctx, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    @staticmethod
    def _create_env(api_gw_is_public: bool, include_s3_bucket_exposed_methods: bool) -> AwsEnvironmentContext:
        s3_bucket = create_empty_entity(S3Bucket, bucket_name='bucket_name')
        lambda_func = create_empty_entity(LambdaFunction)
        agw_method = create_empty_entity(ApiGatewayMethod)
        api_gw = create_empty_entity(RestApiGw)
        integration = create_empty_entity(ApiGatewayIntegration)
        integration.lambda_func_integration = lambda_func

        if include_s3_bucket_exposed_methods:
            agw_method.integration = integration
            agw_method.rest_api_id = 'rest_api_gw_id'
            s3_bucket.exposed_to_agw_methods = [agw_method]

        api_gw.rest_api_gw_id = 'rest_api_gw_id'
        api_gw.is_public = api_gw_is_public

        return AwsEnvironmentContext(s3_buckets=AliasesDict(s3_bucket),
                                     lambda_function_list=[lambda_func],
                                     api_gateway_methods=[agw_method],
                                     rest_api_gw=[api_gw],
                                     api_gateway_integrations=[integration])
