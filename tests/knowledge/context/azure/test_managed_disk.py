from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.disk.azure_managed_disk import ManagedDiskCreateOption, StorageAccountType
from test.knowledge.context.azure_context_test import AzureContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestManagedDisk(AzureContextTest):

    def get_component(self):
        return "managed_disk"

    # Not running drift detection since i am unable to create drift data (permission issue)
    @context(module_path="encrypted_with_disk_encryption_set_resource", test_options=TestOptions(run_drift_detection=False))
    def test_encrypted_with_disk_encryption_set_resource(self, ctx: AzureEnvironmentContext):
        managed_disk = next((disk for disk in ctx.managed_disks if disk.name == 'cr2337001-disk'), None)
        self.assertIsNotNone(managed_disk)
        self.assertEqual(managed_disk.storage_account_type, StorageAccountType.STANDARD_LRS)
        self.assertEqual(managed_disk.create_option, ManagedDiskCreateOption.EMPTY)
        self.assertFalse(managed_disk.disk_encryption_enabled)
        if managed_disk.is_managed_by_iac:
            self.assertEqual(managed_disk.disk_encryption_set_id, 'azurerm_disk_encryption_set.eset.id')
        else:
            self.assertEqual(managed_disk.disk_encryption_set_id, '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/CR2337001-RG/providers/Microsoft.Compute/diskEncryptionSets/cr2337001-deset')
            self.assertEqual(managed_disk.get_cloud_resource_url(),
                             'https://portal.azure.com/#@871cad0f-903e-4648-9655-89b796e7c99e/resource/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/CR2337001-RG/providers/Microsoft.Compute/disks/cr2337001-disk/overview')

    # Not running drift detection since i am unable to create drift data (permission issue)
    @context(module_path="encrypted_with_encryption_settings", test_options=TestOptions(run_drift_detection=False))
    def test_encrypted_with_encryption_settings(self, ctx: AzureEnvironmentContext):
        managed_disk = next((disk for disk in ctx.managed_disks if disk.name == 'cr23371-disk'), None)
        self.assertIsNotNone(managed_disk)
        self.assertEqual(managed_disk.storage_account_type, StorageAccountType.STANDARD_LRS)
        self.assertEqual(managed_disk.create_option, ManagedDiskCreateOption.EMPTY)
        self.assertTrue(managed_disk.disk_encryption_enabled)
        self.assertIsNone(managed_disk.disk_encryption_set_id)

    @context(module_path="not_encrypted_disk")
    def test_not_encrypted_disk(self, ctx: AzureEnvironmentContext):
        managed_disk = next((disk for disk in ctx.managed_disks if disk.name == 'cr2337-disk'), None)
        self.assertIsNotNone(managed_disk)
        self.assertEqual(managed_disk.storage_account_type, StorageAccountType.STANDARD_LRS)
        self.assertEqual(managed_disk.create_option, ManagedDiskCreateOption.EMPTY)
        self.assertFalse(managed_disk.disk_encryption_enabled)
        self.assertIsNone(managed_disk.disk_encryption_set_id)
