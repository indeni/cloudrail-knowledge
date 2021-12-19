from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestCloudWatchLogGroups(AwsContextTest):

    def get_component(self):
        return "cloud_watch_logs"

    # Not running drift-detection, as the KMS policy does not allow reading the KMS data, we have drift for missing entities.
    @context(module_path="encrypted", test_options=TestOptions(run_drift_detection=False))
    def test_encrypted(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.cloud_watch_log_groups), 1)
        log_group = ctx.cloud_watch_log_groups[0]
        self.assertTrue(log_group.server_name)
        self.assertTrue(log_group.kms_encryption)
        self.assertTrue(log_group.arn)
        self.assertTrue(log_group.retention_in_days)
        if not log_group.is_managed_by_iac:
            self.assertEqual(log_group.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2'
                             ':log-groups/log-group/terraform-20201206081938597100000001')

    @context(module_path="non_encrypted")
    def test_non_encrypted(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.cloud_watch_log_groups), 1)
        log_group = ctx.cloud_watch_log_groups[0]
        self.assertTrue(log_group.server_name)
        self.assertFalse(log_group.kms_encryption)
        self.assertTrue(log_group.arn)
        self.assertTrue(log_group.retention_in_days)

    @context(module_path="no_retantion")
    def test_no_retantion(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.cloud_watch_log_groups), 1)
        log_group = ctx.cloud_watch_log_groups[0]
        self.assertTrue(log_group.server_name)
        self.assertFalse(log_group.kms_encryption)
        self.assertTrue(log_group.arn)
        self.assertFalse(log_group.retention_in_days)
        self.assertFalse(log_group.tags)

    @context(module_path="with_tags")
    def test_with_tags(self, ctx: AwsEnvironmentContext):
        log_group = next((log_group for log_group in ctx.cloud_watch_log_groups
                          if log_group.server_name == 'terraform-20210830144217856000000001'
                          or log_group.server_name == 'aws_cloudwatch_log_group.cloudrail-test.name'), None)
        self.assertTrue(log_group.name)
        self.assertFalse(log_group.kms_encryption)
        self.assertTrue(log_group.arn)
        self.assertTrue(log_group.retention_in_days)
        self.assertTrue(log_group.tags)
