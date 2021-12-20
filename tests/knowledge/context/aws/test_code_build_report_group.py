from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestCodeBuildReportGroup(AwsContextTest):

    def get_component(self):
        return "codebuild_report_group"

    @context(module_path="encrypted_at_rest_with_aws_managed_key_by_key_arn", test_options=TestOptions(tf_version='>3.5.0'))
    def test_encrypted_at_rest_with_aws_managed_key_by_key_arn(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.codebuild_report_groups), 1)
        report_group = ctx.codebuild_report_groups[0]
        self.assertEqual(report_group.name, 'codebuild-report-group-non-kms-cmk-encrypted')
        self.assertTrue(report_group.export_config_s3_destination_encryption_key)
        self.assertFalse(report_group.export_config_s3_destination_encryption_disabled)

    @context(module_path="encrypted_at_rest_with_customer_managed_key_creating_key", test_options=TestOptions(tf_version='>3.5.0'))
    def test_encrypted_at_rest_with_customer_managed_key_creating_key(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.codebuild_report_groups), 1)
        report_group = ctx.codebuild_report_groups[0]
        self.assertEqual(report_group.name, 'codebuild-report-group-non-kms-cmk-encrypted')
        self.assertTrue(report_group.export_config_s3_destination_encryption_key)
        self.assertFalse(report_group.export_config_s3_destination_encryption_disabled)

    @context(module_path="basic_with_tags", test_options=TestOptions(tf_version='>3.5.0'))
    def test_basic_with_tags(self, ctx: AwsEnvironmentContext):
        group = next((group for group in ctx.codebuild_report_groups if group.name == 'codebuild-report-group-non-kms-cmk-encrypted'), None)
        self.assertIsNotNone(group)
        self.assertTrue(group.tags)
        if not group.is_managed_by_iac:
            self.assertEqual(group.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/codesuite/codebuild/115553109071/'
                             'testReports/reportGroups/codebuild-report-group-non-kms-cmk-encrypted')
