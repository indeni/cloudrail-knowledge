from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestAzurePostgreSqlServerConfiguration(AzureContextTest):

    def get_component(self):
        return "postgresql_server_configuration"

    @context(module_path="basic")
    def test_postgresql_enforcing_ssl_enabled(self, ctx: AzureEnvironmentContext):
        server1_config = next((config for config in ctx.postgresql_servers_configuration if
                               config.name == 'connection_throttling' and config.server_name == 'cr3692-postgresql-server'), None)
        server2_config = next((config for config in ctx.postgresql_servers_configuration if
                               config.name == 'connection_throttling' and config.server_name == 'cr3692-postgresql-server2'), None)
        self.assertIsNotNone(server1_config and server2_config)
        self.assertEqual(server1_config.value, 'on')
        self.assertEqual(server2_config.value, 'on')
