from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import OperatingSystemType, OsDiskCaching, OsDiskStorageAccountType, SourceImageReference
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import Sku, UpgradePolicyMode
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestAzureVirtualMachineScaleSet(AzureContextTest):

    def get_component(self):
        return "vmss"

    @context(module_path="linux_vmss_v1")
    def test_linux_vmss(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.name == 'lin-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertFalse(scale.disk_settings.os_disk.name)
        self.assertFalse(scale.disk_settings.data_disks)
        self.assertTrue(scale.disk_settings.os_disk.is_managed_disk)
        self.assertTrue(scale.network_interfaces_config)
        self.assertEqual(scale.network_interfaces_config[0].name, 'linux-vm-interface')
        subnet = next((subnet for subnet in ctx.subnets if subnet.name == 'cr2340-snet'), None)
        self.assertIsNotNone(subnet)
        self.assertEqual(scale.network_interfaces_config[0].ip_configurations[0].subnet_id, subnet.get_id())
        if not scale.is_managed_by_iac:
            self.assertEqual(scale.get_cloud_resource_url(),
                             'https://portal.azure.com/#@871cad0f-903e-4648-9655-89b796e7c99e/resource/subscriptions/'
                             '230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/CR2340-RG/providers/Microsoft.Compute/virtualMachineScaleSets/lin-vmss/overview')
        self.assertTrue(len(ctx.virtual_machines), 1)
        virtual_machine = next((vm for vm in ctx.virtual_machines if 'lin-vmss_0' in vm.name), None)
        self.assertIsNotNone(virtual_machine)

    @context(module_path="linux_vmss_with_data_disk")
    def test_linux_vmss_with_data_disk(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.name == 'lin-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertFalse(scale.disk_settings.os_disk.name)
        self.assertTrue(scale.disk_settings.data_disks)
        self.assertTrue(scale.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(len(scale.disk_settings.data_disks), 1)
        self.assertTrue(scale.disk_settings.data_disks[0].is_managed_disk)
        self.assertFalse(scale.disk_settings.data_disks[0].name)

    @context(module_path="no_os_managed_disks_v2")
    def test_no_os_managed_disks(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.name == 'cr2340-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertFalse(scale.disk_settings.os_disk.name)
        self.assertFalse(scale.disk_settings.data_disks)
        self.assertTrue(scale.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(scale.disk_settings.os_disk.caching, OsDiskCaching.READ_WRITE)
        self.assertEqual(scale.disk_settings.os_disk.storage_account_type, OsDiskStorageAccountType.STANDARDLRS)
        self.assertEqual(scale.source_image_reference, SourceImageReference('Canonical', 'UbuntuServer', '16.04-LTS', 'latest'))
        self.assertEqual(scale.upgrade_policy_mode, UpgradePolicyMode.MANUAL)
        self.assertEqual(scale.sku, Sku('Standard_B2s', None, 1))
        self.assertEqual(scale.instances, 1)
        self.assertFalse(scale.disable_password_authentication)
        self.assertTrue(scale.network_interfaces_config)
        self.assertEqual(scale.network_interfaces_config[0].name, 'networkprofile')
        subnet = next((subnet for subnet in ctx.subnets if subnet.name == 'cr2340-snet'), None)
        self.assertIsNotNone(subnet)
        self.assertEqual(scale.network_interfaces_config[0].ip_configurations[0].subnet_id, subnet.get_id())

    @context(module_path="no_os_unmanaged_disk_1")
    def test_no_os_unmanaged_disk(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.name == 'cr2340-vmss2'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertEqual(scale.disk_settings.os_disk.name, 'myosdisk1')
        self.assertFalse(scale.disk_settings.data_disks)
        self.assertFalse(scale.disk_settings.os_disk.is_managed_disk)

    @context(module_path="no_os_using_data_disk_1")
    def test_no_os_using_data_disk(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.name == 'cr2340-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertTrue(scale.disk_settings.os_disk)
        self.assertTrue(scale.disk_settings.data_disks)
        self.assertFalse(scale.disk_settings.data_disks[0].name)
        self.assertTrue(scale.disk_settings.data_disks[0].is_managed_disk)

    @context(module_path="windows_vmss")
    def test_windows_vmss(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.name == 'win-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.WINDOWS)

    @context(module_path="windows_vmss_data_disk")
    def test_windows_vmss_data_disk(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.name == 'win-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.WINDOWS)
        self.assertTrue(scale.disk_settings.data_disks[0].is_managed_disk)
        self.assertFalse(scale.disk_settings.data_disks[0].name)

    @context(module_path="windows_vmss_full_fields")
    def test_windows_vmss_full_fields(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.name == 'cr3672-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.WINDOWS)
        self.assertTrue(scale.disk_settings)
        self.assertFalse(scale.disk_settings.os_disk.name)
        self.assertFalse(scale.disk_settings.data_disks)
        self.assertTrue(scale.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(scale.disk_settings.os_disk.caching, OsDiskCaching.READ_WRITE)
        self.assertEqual(scale.disk_settings.os_disk.storage_account_type, OsDiskStorageAccountType.STANDARDLRS)
        self.assertEqual(scale.source_image_reference, SourceImageReference('MicrosoftWindowsServer', 'WindowsServer', '2016-Datacenter-Server-Core', 'latest'))
        self.assertEqual(scale.upgrade_policy_mode, UpgradePolicyMode.MANUAL)
        self.assertEqual(scale.sku, Sku('Standard_B2s', None, 1))
        self.assertEqual(scale.instances, 1)
        self.assertIsNone(scale.disable_password_authentication)

    @context(module_path="linux_vmss_full_fields")
    def test_linux_vmss_full_fields(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.name == 'cr3674-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertFalse(scale.disk_settings.os_disk.name)
        self.assertFalse(scale.disk_settings.data_disks)
        self.assertTrue(scale.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(scale.disk_settings.os_disk.caching, OsDiskCaching.READ_WRITE)
        self.assertEqual(scale.disk_settings.os_disk.storage_account_type, OsDiskStorageAccountType.STANDARDLRS)
        self.assertEqual(scale.source_image_reference, SourceImageReference('Canonical', 'UbuntuServer', '16.04-LTS', 'latest'))
        self.assertEqual(scale.upgrade_policy_mode, UpgradePolicyMode.MANUAL)
        self.assertEqual(scale.sku, Sku('Standard_B2s', None, 1))
        self.assertEqual(scale.instances, 1)
        self.assertFalse(scale.disable_password_authentication)
