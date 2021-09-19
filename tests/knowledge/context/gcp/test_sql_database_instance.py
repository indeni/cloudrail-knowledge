from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestSqlDatabaseInstance(GcpContextTest):
    def get_component(self):
        return 'sql'

    @context(module_path="ssl_required_true", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_ssl_required_true(self, ctx: GcpEnvironmentContext):
        sql = self._get_sql(ctx)
        self.assertTrue(sql.require_ssl)

    @context(module_path="ssl_required_false", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_ssl_required_false(self, ctx: GcpEnvironmentContext):
        sql = self._get_sql(ctx)
        self.assertFalse(sql.require_ssl)

    @context(module_path="ssl_required_not_specified", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_ssl_required_not_specified(self, ctx: GcpEnvironmentContext):
        sql = self._get_sql(ctx)
        self.assertFalse(sql.require_ssl)

    def _get_sql(self, ctx: GcpEnvironmentContext) -> GcpSqlDatabaseInstance:
        sql = next((sql for sql in ctx.sql_database_instances if sql.name == 'my-sql-instance'), None)
        self.assertIsNotNone(sql)
        return sql
