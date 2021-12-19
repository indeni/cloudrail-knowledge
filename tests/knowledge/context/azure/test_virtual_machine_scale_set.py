from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import OperatingSystemType

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestAzureVirtualMachineScaleSet(AzureContextTest):

    def get_component(self):
        return "vmss"

    @context(module_path="linux_vmss")
    def test_linux_vmss(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.server_name == 'lin-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertFalse(scale.disk_settings.os_disk.server_name)
        self.assertFalse(scale.disk_settings.data_disks)
        self.assertTrue(scale.disk_settings.os_disk.is_managed_disk)
        self.assertTrue(scale.network_interfaces_config)
        self.assertEqual(scale.network_interfaces_config[0].server_name, 'linux-vm-interface')
        subnet = next((subnet for subnet in ctx.subnets if subnet.server_name == 'cr2340-snet'), None)
        self.assertIsNotNone(subnet)
        self.assertEqual(scale.network_interfaces_config[0].ip_configurations[0].subnet_id, subnet.get_id())
        if not scale.is_managed_by_iac:
            self.assertEqual(scale.get_cloud_resource_url(),
                             'https://portal.azure.com/#@871cad0f-903e-4648-9655-89b796e7c99e/resource/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/CR2340-RG/providers/Microsoft.Compute/virtualMachineScaleSets/lin-vmss/overview')
        self.assertTrue(len(ctx.virtual_machines), 1)
        virtual_machine = next((vm for vm in ctx.virtual_machines if 'lin-vmss_0' in vm.server_name), None)
        self.assertIsNotNone(virtual_machine)

    @context(module_path="linux_vmss_with_data_disk")
    def test_linux_vmss_with_data_disk(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.server_name == 'lin-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertFalse(scale.disk_settings.os_disk.server_name)
        self.assertTrue(scale.disk_settings.data_disks)
        self.assertTrue(scale.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(len(scale.disk_settings.data_disks), 1)
        self.assertTrue(scale.disk_settings.data_disks[0].is_managed_disk)
        self.assertFalse(scale.disk_settings.data_disks[0].server_name)

    @context(module_path="no_os_managed_disks")
    def test_no_os_managed_disks(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.server_name == 'cr2340-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertFalse(scale.disk_settings.os_disk.server_name)
        self.assertFalse(scale.disk_settings.data_disks)
        self.assertTrue(scale.disk_settings.os_disk.is_managed_disk)
        self.assertTrue(scale.network_interfaces_config)
        self.assertEqual(scale.network_interfaces_config[0].server_name, 'networkprofile')
        subnet = next((subnet for subnet in ctx.subnets if subnet.server_name == 'cr2340-snet'), None)
        self.assertIsNotNone(subnet)
        self.assertEqual(scale.network_interfaces_config[0].ip_configurations[0].subnet_id, subnet.get_id())

    @context(module_path="no_os_unmanaged_disk")
    def test_no_os_unmanaged_disk(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.server_name == 'cr2340-vmss2'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertEqual(scale.disk_settings.os_disk.server_name, 'myosdisk1')
        self.assertFalse(scale.disk_settings.data_disks)
        self.assertFalse(scale.disk_settings.os_disk.is_managed_disk)

    @context(module_path="no_os_using_data_disk")
    def test_no_os_using_data_disk(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.server_name == 'cr2340-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.LINUX)
        self.assertTrue(scale.disk_settings)
        self.assertTrue(scale.disk_settings.os_disk)
        self.assertTrue(scale.disk_settings.data_disks)
        self.assertFalse(scale.disk_settings.data_disks[0].server_name)
        self.assertTrue(scale.disk_settings.data_disks[0].is_managed_disk)

    @context(module_path="windows_vmss")
    def test_windows_vmss(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.server_name == 'win-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.WINDOWS)

    @context(module_path="windows_vmss_data_disk")
    def test_windows_vmss_data_disk(self, ctx: AzureEnvironmentContext):
        scale = next((scale for scale in ctx.virtual_machines_scale_sets if scale.server_name == 'win-vmss'))
        self.assertIsNotNone(scale)
        self.assertEqual(scale.os_type, OperatingSystemType.WINDOWS)
        self.assertTrue(scale.disk_settings.data_disks[0].is_managed_disk)
        self.assertFalse(scale.disk_settings.data_disks[0].server_name)
