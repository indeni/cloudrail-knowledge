from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestGlueDataCatalogCrawler(AwsContextTest):

    def get_component(self):
        return "glue_data_catalog"

    @context(module_path="basic_resources")
    def test_basic_resources(self, ctx: AwsEnvironmentContext):
        crawler = next((crawler for crawler in ctx.glue_data_catalog_crawlers if crawler.crawler_name == 'cloudrail_table_crawler'), None)
        self.assertIsNotNone(crawler)
        self.assertEqual(crawler.database_name, 'cloudrail_table_database')
        self.assertFalse(crawler.tags)
        self.assertEqual(crawler.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/glue/home?region=us-east-1#crawler:name=cloudrail_table_crawler')

    @context(module_path="crawler_with_tags")
    def test_crawler_with_tags(self, ctx: AwsEnvironmentContext):
        crawler = next((crawler for crawler in ctx.glue_data_catalog_crawlers if crawler.crawler_name == 'cloudrail_table_crawler'), None)
        self.assertIsNotNone(crawler)
        self.assertTrue(crawler.tags)
        self.assertTrue(crawler.arn)
