from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server import PostgreSqlServerVersion

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

    @context(module_path="basic")
    def test_postgresql_server(self, ctx: AzureEnvironmentContext):
        server1 = ctx.postgresql_servers.get('cr3692-postgresql-server')
        server2 = ctx.postgresql_servers.get('cr3692-postgresql-server2')
        self.assertIsNotNone(server1 and server2)
        self.assertTrue(server1.ssl_enforcement_enabled)
        self.assertTrue(server1.auto_grow_enabled)
        self.assertFalse(server1.geo_redundant_backup_enabled)
        self.assertFalse(server1.infrastructure_encryption_enabled)
        self.assertEqual(server1.administrator_login, "psqladminun")
        self.assertEqual(server1.version, PostgreSqlServerVersion.VERSION_11)
        self.assertEqual(server1.sku_name, "GP_Gen5_2")
        self.assertEqual(server1.identity.type, "SystemAssigned")
        self.assertEqual(server1.ssl_minimal_tls_version_enforced, "TLS1_2")
        self.assertEqual(server1.storage_mb, 5120)
        self.assertEqual(server1.backup_retention_days, 7)
        if server1.postgresql_configuration.name == 'connection_throttling':
            self.assertTrue(server1.postgresql_configuration.value == 'on')

        self.assertTrue(server2.public_network_access_enabled)
        self.assertTrue(server2.ssl_enforcement_enabled)
        self.assertTrue(server2.auto_grow_enabled)
        self.assertFalse(server2.infrastructure_encryption_enabled)
        self.assertEqual(server2.version, PostgreSqlServerVersion.VERSION_11)
        self.assertEqual(server2.sku_name, "GP_Gen5_2")
        self.assertEqual(server2.ssl_minimal_tls_version_enforced, "TLS1_2")
        if server2.postgresql_configuration.name == 'connection_throttling':
            self.assertTrue(server2.postgresql_configuration.value == 'on')
