from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestFsxWindowsFileSystem(AwsContextTest):

    def get_component(self):
        return "fsx_windows_file_system"

    @context(module_path="encrypted_with_customer_managed_cmk_creating_key")
    def test_encrypted_with_customer_managed_cmk_creating_key(self, ctx: AwsEnvironmentContext):
        kms_key = next((kms_key for kms_key in ctx.kms_keys), None)
        self.assertIsNotNone(kms_key)
        self.assertEqual(kms_key.key_manager, KeyManager.CUSTOMER)
        fsx_windows_file_system = next((fsx_windows_file_system for fsx_windows_file_system in ctx.fsx_windows_file_systems), None)
        self.assertIsNotNone(fsx_windows_file_system)
        self.assertEqual(fsx_windows_file_system.kms_data, kms_key)

    @context(module_path="encrypted_with_aws_managed_cmk_by_key_arn")
    def test_encrypted_with_aws_managed_cmk_by_key_arn(self, ctx: AwsEnvironmentContext):
        fsx_windows_file_system = next((fsx_windows_file_system for fsx_windows_file_system in ctx.fsx_windows_file_systems), None)
        self.assertIsNotNone(fsx_windows_file_system)
        self.assertTrue(fsx_windows_file_system.kms_data is None or fsx_windows_file_system.kms_data.key_manager == KeyManager.AWS)
        self.assertIsNotNone(fsx_windows_file_system.kms_key_id)

    @context(module_path="encrypted_with_aws_managed_cmk_by_default")
    def test_encrypted_with_aws_managed_cmk_by_default(self, ctx: AwsEnvironmentContext):
        fsx_windows_file_system = next((fsx_windows_file_system for fsx_windows_file_system in ctx.fsx_windows_file_systems), None)
        self.assertIsNotNone(fsx_windows_file_system)
        self.assertTrue(fsx_windows_file_system.kms_data is None or fsx_windows_file_system.kms_data.key_manager == KeyManager.AWS)
