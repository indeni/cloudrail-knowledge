from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from tests.knowledge.context.gcp_context_test import GcpNoCloudAccountContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestNoCloudAccount(GcpNoCloudAccountContextTest):

    def get_component(self):
        return 'no_cloud_account'

    # No drift detection, as this scenario is without cloud account
    @context(module_path="sql", test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_sql_no_cloud_account(self, ctx: GcpEnvironmentContext):
        sql = next((sql for sql in ctx.sql_database_instances if sql.name == 'my-sql-instance'), None)
        self.assertIsNotNone(sql)
        self.assertEqual(sql.project_id, 'no-cloud-account-used')
