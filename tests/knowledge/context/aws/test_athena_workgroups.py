from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestAthenaWorkgroups(AwsContextTest):

    def get_component(self):
        return "athena"

    @context(module_path="encrypted_work_groups", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_encrypted_work_groups(self, ctx: AwsEnvironmentContext):
        for workgroup in ctx.athena_workgroups:
            if workgroup.name == 'cloudrail-wg-encrypted-sse-s3':
                self.assertTrue(workgroup.enforce_workgroup_config)
                self.assertTrue(workgroup.encryption_config)
                self.assertEqual(workgroup.state, 'ENABLED')
                self.assertFalse(workgroup.tags)

    @context(module_path="encrypted_cse_kms_cmk", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_encrypted_cse_kms_cmk(self, ctx: AwsEnvironmentContext):
        for workgroup in ctx.athena_workgroups:
            if workgroup.name == 'cloudrail-wg-encrypted-cse-kms-cmk':
                self.assertTrue(workgroup.enforce_workgroup_config)
                self.assertTrue(workgroup.encryption_config)
                self.assertEqual(workgroup.state, 'ENABLED')
                self.assertEqual(workgroup.encryption_option, 'CSE_KMS')
                self.assertEqual((workgroup.kms_key_arn is None and workgroup.kms_key_id is None), workgroup.kms_data is None)

    @context(module_path="encrypted_work_gropup_with_tags")
    def test_encrypted_work_gropup_with_tags(self, ctx: AwsEnvironmentContext):
        workgroup = next((workgroup for workgroup in ctx.athena_workgroups if workgroup.name == 'cloudrail-wg-encrypted-sse-s3'), None)
        self.assertIsNotNone(workgroup)
        self.assertTrue(workgroup.tags)
        self.assertTrue(workgroup.arn)
        self.assertEqual(workgroup.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/athena/workgroup/view-details/cloudrail-wg-encrypted-sse-s3/home?region=us-east-1')
