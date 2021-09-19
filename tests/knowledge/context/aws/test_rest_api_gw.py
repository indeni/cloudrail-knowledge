from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import ApiGatewayIntegration, IntegrationType
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import RestApiMethods
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestRestApiGw(AwsContextTest):

    def get_component(self):
        return "rest_api_gw"

    @context(module_path="encrypted_rest_api")
    def test_encrypted_rest_api(self, ctx: AwsEnvironmentContext):
        api_gw = ctx.rest_api_gw[0]
        self.assertTrue(api_gw.rest_api_gw_id)
        self.assertTrue(api_gw.method_settings.caching_enabled)
        self.assertTrue(api_gw.method_settings.caching_encrypted)
        self.assertEqual(api_gw.method_settings.stage_name, 'prod')
        self.assertEqual(api_gw.method_settings.http_method, RestApiMethods.GET)
        self.assertFalse(api_gw.tags)
        if not api_gw.is_managed_by_iac:
            self.assertEqual(api_gw.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/apigateway/home?region=us-east-1#/apis/g2xsexmoik/resources/')

    @context(module_path="non_encrypted_rest_api_cache_enabled")
    def test_non_encrypted_rest_api_cache_enabled(self, ctx: AwsEnvironmentContext):
        api_gw = ctx.rest_api_gw[0]
        self.assertTrue(api_gw.rest_api_gw_id)
        self.assertTrue(api_gw.method_settings.caching_enabled)
        self.assertFalse(api_gw.method_settings.caching_encrypted)
        self.assertEqual(api_gw.method_settings.stage_name, 'prod')
        self.assertEqual(api_gw.method_settings.http_method, RestApiMethods.GET)

    @context(module_path="non_encrypted_rest_api_cache_disabled")
    def test_non_encrypted_rest_api_cache_disabled(self, ctx: AwsEnvironmentContext):
        api_gw = ctx.rest_api_gw[0]
        self.assertTrue(api_gw.rest_api_gw_id)
        self.assertFalse(api_gw.method_settings.caching_enabled)
        self.assertFalse(api_gw.method_settings.caching_encrypted)
        self.assertEqual(api_gw.method_settings.stage_name, 'prod')
        self.assertEqual(api_gw.method_settings.http_method, RestApiMethods.GET)

    @context(module_path="not_secure_policy")
    def test_not_secure_policy(self, ctx: AwsEnvironmentContext):
        for api_gw in ctx.rest_api_gw_policies:
            self.assertTrue(api_gw.rest_api_gw_id)
            self.assertEqual(api_gw.statements[0].effect, StatementEffect.ALLOW)
            self.assertEqual(api_gw.statements[0].actions, ['execute-api:*'])

    @context(module_path="tls_good_encryption")
    def test_tls_good_encryption(self, ctx: AwsEnvironmentContext):
        for api_gw in ctx.rest_api_gw_mappings:
            self.assertTrue(api_gw.api_id)
            self.assertTrue(api_gw.domain_name)

    @context(module_path="tls_bad_encryption")
    def test_tls_bad_encryption(self, ctx: AwsEnvironmentContext):
        api_gw = next((api_gw for api_gw in ctx.rest_api_gw_domains if api_gw.security_policy == 'TLS_1_0'), None)
        self.assertIsNotNone(api_gw)
        self.assertTrue(api_gw.domain_name)

    @context(module_path="tls_bad_encryption")
    def test_tls_bad_encryption_relations(self, ctx: AwsEnvironmentContext):
        api_gw = next((api_gw for api_gw in ctx.rest_api_gw if api_gw.domain.security_policy == 'TLS_1_0'), None)
        self.assertIsNotNone(api_gw)
        self.assertTrue(api_gw.domain.domain_name)

    @context(module_path="encrypted_rest_api_with_tags")
    def test_encrypted_rest_api_with_tags(self, ctx: AwsEnvironmentContext):
        api_gw = next((rest_api for rest_api in ctx.rest_api_gw
                       if rest_api.api_gw_name == 'api-gw-cache-encrypted'), None)
        self.assertIsNotNone(api_gw)
        self.assertTrue(api_gw.tags)

    @context(module_path="domain_with_tags")
    def test_domain_with_tags(self, ctx: AwsEnvironmentContext):
        api_domain = next((api_domain for api_domain in ctx.rest_api_gw_domains if api_domain.security_policy == 'TLS_1_2'), None)
        self.assertIsNotNone(api_domain)
        self.assertTrue(api_domain.tags)

    @context(module_path="api-gateway-method")
    def test_api_gateway_method(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.api_gateway_methods), 1)
        agw_method: ApiGatewayMethod = ctx.api_gateway_methods[0]
        self.assertEqual(agw_method.account, self.DUMMY_ACCOUNT_ID)
        self.assertEqual(agw_method.region, self.REGION)
        self.assertEqual(agw_method.http_method, RestApiMethods.ANY)
        self.assertEqual(agw_method.authorization, 'NONE')

        if agw_method.is_managed_by_iac:
            self.assertEqual(agw_method.rest_api_id, 'aws_api_gateway_rest_api.my-api-gateway.id')
            self.assertEqual(agw_method.resource_id, 'aws_api_gateway_resource.my-api-gateway-resource.id')
        else:
            self.assertEqual(agw_method.rest_api_id, 'z2in2i6ddg')
            self.assertEqual(agw_method.resource_id, 'dmg1jt')

    @context(module_path="api-gateway-integration")
    def test_api_gateway_integration(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.api_gateway_methods), 1)
        agw_method: ApiGatewayMethod = ctx.api_gateway_methods[0]
        self.assertIsNotNone(agw_method.integration)
        integration: ApiGatewayIntegration = agw_method.integration
        self.assertEqual(integration.integration_http_method, RestApiMethods.POST)
        self.assertEqual(integration.integration_type, IntegrationType.AWS)
        self.assertIsNotNone(integration.lambda_func_integration)
        self.assertEqual(len(ctx.lambda_function_list), 1)
        lambda_func: LambdaFunction = ctx.lambda_function_list[0]
        self.assertEqual(integration.lambda_func_integration, lambda_func)

    @context(module_path="api-gateway-method-auth-not-none")
    def test_api_gateway_method_auth_not_none(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.api_gateway_methods), 1)
        agw_method: ApiGatewayMethod = ctx.api_gateway_methods[0]
        self.assertEqual(agw_method.authorization, 'AWS_IAM')

    @context(module_path="api_stage_xray_trace_enable")
    def test_api_stage_xray_trace_enable(self, ctx: AwsEnvironmentContext):
        stage = next((stage for stage in ctx.rest_api_stages if stage.stage_name == 'example'), None)
        self.assertIsNotNone(stage)
        self.assertTrue(stage.api_gw_id)
        self.assertTrue(stage.xray_tracing_enabled)
        if not stage.is_managed_by_iac:
            self.assertEqual(stage.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/apigateway/home?region=us-east-1#/apis/yp3eslxf36/stages/example')

    @context(module_path="api_stage_xray_trace_disable")
    def test_api_stage_xray_trace_disable(self, ctx: AwsEnvironmentContext):
        stage = next((stage for stage in ctx.rest_api_stages if stage.stage_name == 'example'), None)
        self.assertIsNotNone(stage)
        self.assertTrue(stage.api_gw_id)
        self.assertFalse(stage.xray_tracing_enabled)
        self.assertIsNone(stage.access_logs)
        rest_api = next((api for api in ctx.rest_api_gw if api.api_gw_name == 'api-test-xray'), None)
        self.assertIsNotNone(rest_api)
        self.assertTrue(len(rest_api.api_gw_stages) > 0)

    @context(module_path="with_access_logs")
    def test_with_access_logs(self, ctx: AwsEnvironmentContext):
        stage = next((stage for stage in ctx.rest_api_stages if stage.stage_name == 'example'), None)
        self.assertIsNotNone(stage)
        self.assertTrue(stage.access_logs)
        self.assertTrue(stage.access_logs.destination_arn)
        self.assertEqual(stage.access_logs.format, '$context.requestId')
