from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from test.knowledge.context.azure_context_test import AzureContextTest
from test.knowledge.context.test_context_annotation import context


class TestMySqlServer(AzureContextTest):

    def get_component(self):
        return "my_sql_server"

    @context(module_path="ssl_enforce_enabled")
    def test_ssl_enforce_enabled(self, ctx: AzureEnvironmentContext):
        my_sql_server = ctx.my_sql_servers.get('cr2466-mysqlserver')
        self.assertIsNotNone(my_sql_server)
        self.assertTrue(my_sql_server.ssl_enforcement_enabled)

    @context(module_path="ssl_enforce_disabled")
    def test_ssl_enforce_disabled(self, ctx: AzureEnvironmentContext):
        my_sql_server = ctx.my_sql_servers.get('cr2466-mysqlserver')
        self.assertIsNotNone(my_sql_server)
        self.assertFalse(my_sql_server.ssl_enforcement_enabled)
