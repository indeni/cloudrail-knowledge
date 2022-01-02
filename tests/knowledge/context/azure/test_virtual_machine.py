from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import OperatingSystemType, OsDiskCaching, OsDiskStorageAccountType, SourceImageReference

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestAzureVirtualMachine(AzureContextTest):

    def get_component(self):
        return "virtual_machine"

    @context(module_path="no_os_with_vm_extension")
    def test_no_os_with_vm_extension(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'))
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.WINDOWS)
        self.assertEqual(vm.disk_settings.data_disks, [])
        self.assertTrue(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(vm.disk_settings.os_disk.caching, OsDiskCaching.READ_WRITE)
        self.assertEqual(vm.disk_settings.os_disk.storage_account_type, OsDiskStorageAccountType.STANDARDLRS)
        self.assertEqual(vm.disk_settings.os_disk.name, 'myosdisk1')
        self.assertEqual(vm.sku, 'Standard_B2s')
        self.assertEqual(vm.source_image_reference, SourceImageReference('MicrosoftWindowsServer', 'WindowsServer', '2019-Datacenter', 'latest'))
        self.assertFalse(vm.disable_password_authentication)
        self.assertEqual(len(vm.network_interfaces), 1)
        self.assertEqual(len(vm.extensions), 1)
        self.assertEqual(vm.extensions[0].publisher, 'Microsoft.Azure.Security')

    @context(module_path="linux_vm_with_extension")
    def test_linux_vm_with_extension(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'), None)
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.LINUX)
        self.assertEqual(len(vm.network_interfaces), 1)
        self.assertEqual(vm.disk_settings.data_disks, [])
        self.assertTrue(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(vm.disk_settings.os_disk.caching, OsDiskCaching.READ_WRITE)
        self.assertEqual(vm.disk_settings.os_disk.storage_account_type, OsDiskStorageAccountType.STANDARDLRS)
        if vm.is_managed_by_iac:
            self.assertEqual(vm.disk_settings.os_disk.name, 'azurerm_linux_virtual_machine.main.os_disk.name')
        else:
            self.assertEqual(vm.disk_settings.os_disk.name, 'cr2460-vm_OsDisk_1_a8f9759cd9164d5eb9f3fbb42efa9827')
        self.assertEqual(vm.sku, 'Standard_B2s')
        self.assertEqual(vm.source_image_reference, SourceImageReference('Canonical', 'UbuntuServer', '16.04-LTS', 'latest'))
        self.assertFalse(vm.disable_password_authentication)
        self.assertEqual(len(vm.extensions), 1)
        self.assertEqual(vm.extensions[0].publisher, 'Microsoft.Azure.Extensions')
        self.assertEqual(vm.extensions[0].tags, {'environment': 'Production'})

    @context(module_path="windows_vm_with_extension")
    def test_windows_vm_with_extension(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'))
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.WINDOWS)
        self.assertIsNone(vm.disable_password_authentication)
        self.assertEqual(len(vm.network_interfaces), 1)
        self.assertEqual(len(vm.extensions), 1)
        self.assertEqual(vm.extensions[0].publisher, 'Microsoft.Azure.Security')

    @context(module_path="no_os_managed_disk")
    def test_no_os_managed_disk(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2340-vm'))
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.LINUX)
        self.assertIsNotNone(vm.disk_settings)
        self.assertTrue(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(vm.disk_settings.os_disk.name, 'myosdisk1')
        self.assertFalse(vm.disk_settings.data_disks)

    @context(module_path="no_os_vm_unmanaged_disk")
    def test_no_os_vm_unmanaged_disk(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2340-vm'))
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.LINUX)
        self.assertIsNotNone(vm.disk_settings)
        self.assertFalse(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(vm.disk_settings.os_disk.name, 'myosdisk1')
        self.assertEqual(vm.disk_settings.data_disks, [])

    @context(module_path="no_os_vm_with_data_disks")
    def test_no_os_vm_with_data_disks(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'))
        self.assertIsNotNone(vm)
        self.assertIsNotNone(vm.disk_settings)
        self.assertTrue(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(vm.disk_settings.os_disk.name, 'myosdisk1')
        self.assertEqual(len(vm.disk_settings.data_disks), 2)
        self.assertTrue(all(data_disk.name in ('testdatadisk', 'testdatadisk2') for data_disk in vm.disk_settings.data_disks))
        self.assertTrue(all(data_disk.is_managed_disk for data_disk in vm.disk_settings.data_disks))

    @context(module_path="no_os_both_disks_unmanaged")
    def test_no_os_both_disks_unmanaged(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'))
        self.assertIsNotNone(vm)
        self.assertIsNotNone(vm.disk_settings)
        self.assertFalse(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(len(vm.disk_settings.data_disks), 1)
        self.assertTrue(all(not data_disk.is_managed_disk for data_disk in vm.disk_settings.data_disks))
