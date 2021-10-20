from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestAzurePostgreSqlServer(AzureContextTest):

    def get_component(self):
        return "postgresql_server"

    @context(module_path="postgresql_enforcing_ssl_enabled")
    def test_postgresql_enforcing_ssl_enabled(self, ctx: AzureEnvironmentContext):
        server = ctx.postgresql_servers.get('cr2467-postgresql-server')
        self.assertIsNotNone(server)
        self.assertTrue(server.ssl_enforcement_enabled)

    @context(module_path="postgresql_enforcing_ssl_not_enabled")
    def test_postgresql_enforcing_ssl_not_enabled(self, ctx: AzureEnvironmentContext):
        server = ctx.postgresql_servers.get('cr2467-postgresql-server')
        self.assertIsNotNone(server)
        self.assertFalse(server.ssl_enforcement_enabled)
