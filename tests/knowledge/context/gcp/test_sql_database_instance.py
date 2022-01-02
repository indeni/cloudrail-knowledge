from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSqlDatabaseInstance(GcpContextTest):
    def get_component(self):
        return 'sql'

    @context(module_path="ssl_required_true")
    def test_ssl_required_true(self, ctx: GcpEnvironmentContext):
        sql = self._get_sql(ctx)
        self.assertIsNotNone(sql.settings)
        self.assertIsNotNone(sql.settings.ip_configuration)
        self.assertTrue(sql.settings.ip_configuration.require_ssl)

    @context(module_path="ssl_required_false")
    def test_ssl_required_false(self, ctx: GcpEnvironmentContext):
        sql = self._get_sql(ctx)
        self.assertIsNotNone(sql.settings)
        self.assertIsNotNone(sql.settings.ip_configuration)
        self.assertFalse(sql.settings.ip_configuration.require_ssl)

    @context(module_path="ssl_required_not_specified")
    def test_ssl_required_not_specified(self, ctx: GcpEnvironmentContext):
        sql = self._get_sql(ctx)
        self.assertIsNotNone(sql.settings)
        self.assertIsNotNone(sql.settings.ip_configuration)
        self.assertFalse(sql.settings.ip_configuration.require_ssl)

    def _get_sql(self, ctx: GcpEnvironmentContext) -> GcpSqlDatabaseInstance:
        sql = next((sql for sql in ctx.sql_database_instances if sql.name in ('my-sql-instance', 'my-sql-instance-labels')), None)
        self.assertIsNotNone(sql)
        return sql

    @context(module_path="ssl_required_true_with_labels")
    def test_ssl_required_true_with_labels(self, ctx: GcpEnvironmentContext):
        sql = self._get_sql(ctx)
        self.assertIsNotNone(sql.settings)
        self.assertIsNotNone(sql.labels)
        self.assertTrue(key in ('environment_hashcode', 'name') for key in sql.labels.keys())
