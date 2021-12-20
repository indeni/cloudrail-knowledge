from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server import PostgreSqlServerVersion

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestAzurePostgreSqlServerConfiguration(AzureContextTest):

    def get_component(self):
        return "postgresql_server_configuration"

    @context(module_path="basic", test_options=TestOptions(run_drift_detection=False))
    def test_postgresql_enforcing_ssl_enabled(self, ctx: AzureEnvironmentContext):
        server1_config = ctx.postgresql_servers_configuration.get('connection_throttling_cr3692-postgresql-server')
        server2_config = ctx.postgresql_servers_configuration.get('connection_throttling_cr3692-postgresql-server2')
        self.assertIsNotNone(server1_config and server2_config)
        self.assertEqual(server1_config.value, 'on')
        self.assertEqual(server2_config.value, 'on')
