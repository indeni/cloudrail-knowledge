from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import IntegrationType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import RestApiMethod

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestApiGatewayV2Integration(AwsContextTest):

    def get_component(self):
        return "api_gateway_v2"

    @context(module_path="with_vpc_link")
    def test_with_vpc_link(self, ctx: AwsEnvironmentContext):
        integration = next((integration for integration in ctx.api_gateway_v2_integrations
                            if integration.rest_api_id == 'c24d67urkj'
                            or integration.integration_type == IntegrationType.HTTP_PROXY), None)
        self.assertIsNotNone(integration)
        self.assertTrue(integration.integration_id)
        self.assertTrue(integration.connection_id)
        self.assertTrue(integration.uri)
        self.assertEqual(integration.integration_http_method, RestApiMethod.GET)
        self.assertEqual(integration.integration_type, IntegrationType.HTTP_PROXY)
        if not integration.is_managed_by_iac:
            self.assertEqual(integration.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/apigateway/main/develop/integrations/attach?api=c24d67urkj&region=us-east-1')
