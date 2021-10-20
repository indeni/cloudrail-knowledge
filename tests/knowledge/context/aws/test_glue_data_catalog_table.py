from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestGlueDataCatalogTable(AwsContextTest):

    def get_component(self):
        return "glue_data_catalog"

    @context(module_path="basic_resources")
    def test_basic_resources(self, ctx: AwsEnvironmentContext):
        crawler = next((crawler for crawler in ctx.glue_data_catalog_tables if crawler.table_name == 'cloudrail_table'), None)
        self.assertIsNotNone(crawler)
        self.assertEqual(crawler.database_name, 'cloudrail_table_database')
        if not crawler.is_managed_by_iac:
            self.assertEqual(crawler.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/glue/home?region=us-east-1#'
                             'table:catalog=115553109071;name=cloudrail_table;namespace=cloudrail_table_database')
