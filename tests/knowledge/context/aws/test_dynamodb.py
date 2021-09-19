from cloudrail.knowledge.context.aws.resources.dynamodb.dynamodb_table import DynamoDbTable, BillingMode, TableFieldType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestDynamoDb(AwsContextTest):

    def get_component(self):
        return "dynamodb"

    @context(module_path="cloud-mapper-billing-mode-pay-per-request")
    def test_cloud_mapper_table_billing_mode_pay_per_request(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.dynamodb_table_list), 1)
        for table in ctx.dynamodb_table_list:
            self._verify_billing_mode_pay_per_request(table)
            self.assertEqual(table.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=GameScores;tab=overview')

    @context(module_path="cloud-mapper-billing-mode-provisioned")
    def test_cloud_mapper_table_billing_mode_provisioned(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.dynamodb_table_list), 1)
        for table in ctx.dynamodb_table_list:
            self._verify_billing_mode_provisioned(table)
            self.assertFalse(table.tags)

    def _verify_billing_mode_provisioned(self, table: DynamoDbTable):
        self.assertEqual(table.billing_mode, BillingMode.PROVISIONED)
        self.assertEqual(table.sort_key, "GameTitle")
        self.assertEqual(table.write_capacity, 10)
        self.assertEqual(table.read_capacity, 5)
        self._verify_table_attributes(table)

    def _verify_billing_mode_pay_per_request(self, table: DynamoDbTable):
        self.assertEqual(table.billing_mode, BillingMode.PAY_PER_REQUEST)
        self.assertIsNone(table.sort_key)
        self.assertEqual(table.write_capacity, 0)
        self.assertEqual(table.read_capacity, 0)
        self._verify_table_attributes(table)

    def _verify_table_attributes(self, table: DynamoDbTable):
        self.assertTrue(table.table_name.__contains__("GameScores"))
        self.assertEqual(table.region, "us-east-1")
        self.assertEqual(table.partition_key, "UserId")
        for attr in table.fields_attributes:
            self.assertTrue(attr.name == "UserId" or attr.name == "GameTitle")
            self.assertEqual(attr.type, TableFieldType.STRING)

    @context(module_path="with_tags")
    def test_cloud_mapper_table_billing_mode_provisioned_with_tags(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.dynamodb_table_list), 1)
        for table in ctx.dynamodb_table_list:
            self._verify_billing_mode_provisioned(table)
            self.assertTrue(table.tags)

    @context(module_path="encryption/no_encryption_at_all")
    def test_no_encryption_at_all(self, ctx: AwsEnvironmentContext):
        table = next((table for table in ctx.dynamodb_table_list if table.table_name == 'cloudrail-test'), None)
        self.assertIsNotNone(table)
        self.assertFalse(table.server_side_encryption)
        self.assertFalse(table.kms_key_id)
        self.assertFalse(table.kms_data)

    @context(module_path="encryption/encrypted_default_aws_managed")
    def test_encrypted_default_aws_managed(self, ctx: AwsEnvironmentContext):
        table = next((table for table in ctx.dynamodb_table_list if table.table_name == 'cloudrail-test'), None)
        self.assertIsNotNone(table)
        self.assertTrue(table.server_side_encryption)
        if not table.is_managed_by_iac:
            self.assertTrue(table.kms_key_id)
        else:
            self.assertIsNone(table.kms_key_id)
        self.assertTrue(table.kms_data)

    @context(module_path="encryption/encrypted_default_aws_by_key_arn", base_scanner_data_for_iac='account-data-dynamodb-table-kms-keys',
             test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_encrypted_default_aws_by_key_arn(self, ctx: AwsEnvironmentContext):
        table = next((table for table in ctx.dynamodb_table_list if table.table_name == 'cloudrail-test'), None)
        self.assertIsNotNone(table)
        self.assertTrue(table.server_side_encryption)
        self.assertTrue(table.kms_key_id)
        self.assertTrue(table.kms_data)

    @context(module_path="encryption/encrypted_customer_managed_new_key")
    def test_encrypted_customer_managed_new_key(self, ctx: AwsEnvironmentContext):
        table = next((table for table in ctx.dynamodb_table_list if table.table_name == 'cloudrail-test'), None)
        self.assertIsNotNone(table)
        self.assertTrue(table.server_side_encryption)
        self.assertTrue(table.kms_key_id)
        self.assertTrue(table.kms_data)
