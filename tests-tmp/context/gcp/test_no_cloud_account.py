from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from test.knowledge.context.gcp_context_test import GcpNoCloudAccountContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestNoCloudAccount(GcpNoCloudAccountContextTest):

    def get_component(self):
        return 'no_cloud_account'

    @context(module_path="sql", test_options=TestOptions(run_cloudmapper=False, always_use_cache_on_jenkins=True))
    def test_sql_no_cloud_account(self, ctx: GcpEnvironmentContext):
        sql = next((sql for sql in ctx.sql_database_instances if sql.name == 'my-sql-instance'), None)
        self.assertIsNotNone(sql)
        self.assertEqual(sql.project_id, 'no-cloud-account-used')
