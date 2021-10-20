from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestAthenaDatabase(AwsContextTest):

    def get_component(self):
        return "athena_database"

    @context(module_path="with_encryption", test_options=TestOptions(run_cloudmapper=False))
    def test_with_encryption(self, ctx: AwsEnvironmentContext):
        database = next((db for db in ctx.athena_databases if db.database_name == 'athena_test_encrypted'), None)
        self.assertIsNotNone(database)
        self.assertEqual(database.bucket, 'aws_s3_bucket.test.bucket')
        self.assertEqual(database.encryption_option, 'SSE_S3')
        self.assertIsNone(database.kms_key_encryption)

    @context(module_path="not_encrypted", test_options=TestOptions(run_cloudmapper=False))
    def test_not_encrypted(self, ctx: AwsEnvironmentContext):
        database = next((db for db in ctx.athena_databases if db.database_name == 'athena_test_non_encrypted'), None)
        self.assertIsNotNone(database)
        self.assertEqual(database.bucket, 'aws_s3_bucket.test.bucket')
        self.assertIsNone(database.encryption_option)
        self.assertIsNone(database.kms_key_encryption)
