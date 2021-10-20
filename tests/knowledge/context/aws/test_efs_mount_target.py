from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestEfsMountTarget(AwsContextTest):

    def get_component(self):
        return "efs/efs_mount_target"

    @context(module_path="basic")
    def test_basic(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.efs_mount_targets), 1)
        for efs in ctx.efs_mount_targets:
            if not efs.is_managed_by_iac:
                self.assertTrue(len(efs.security_groups_ids), 1)
                self.assertEqual(efs.security_groups_ids, ['sg-0dfc190f158ec7e5b'])
                self.assertEqual(efs.efs_id, 'fs-655b8ed1')
                self.assertEqual(efs.eni_id, 'eni-048fdd3941f7d005f')
                self.assertEqual(efs.mount_target_id, 'fsmt-739a3cc6')
                self.assertEqual(efs.subnet_id, 'subnet-09c579e2e179ea0f0')
            else:
                self.assertTrue(efs.security_groups_ids)
                self.assertTrue(efs.efs_id)
                self.assertTrue(efs.eni_id)
                self.assertTrue(efs.mount_target_id)
                self.assertTrue(efs.subnet_id)

    @context(module_path="networking_using_security_group")
    def test_networking_using_security_group(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.efs_mount_targets), 1)
        for efs in ctx.efs_mount_targets:
            if not efs.is_managed_by_iac:
                self.assertTrue(len(efs.security_groups_ids), 1)
                self.assertEqual(efs.security_groups_ids, ['sg-08a4daaf22facb7ea'])
                self.assertEqual(efs.efs_id, 'fs-a57da811')
                self.assertEqual(efs.eni_id, 'eni-057257f88ad1426b8')
                self.assertEqual(efs.mount_target_id, 'fsmt-786fc9cd')
                self.assertEqual(efs.subnet_id, 'subnet-0b7a3bc41654db60d')
                self.assertEqual(efs.get_cloud_resource_url(),
                                 'https://console.aws.amazon.com/efs/home?region=us-east-1#/file-systems/fs-a57da811?tabId=mounts')
            else:
                self.assertTrue(efs.security_groups_ids)
                self.assertTrue(len(efs.security_groups_ids), 1)
                self.assertTrue(efs.efs_id)
                self.assertTrue(efs.eni_id)
                self.assertTrue(efs.mount_target_id)
                self.assertTrue(efs.subnet_id)
