from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestVmssExtension(AzureContextTest):

    def get_component(self):
        return "vmss_extension"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        vmss_ext = next((ext for ext in ctx.vms_extentions if ext.name == 'example'))
        self.assertIsNotNone(vmss_ext)
        self.assertEqual(vmss_ext.publisher, 'Microsoft.Azure.Diagnostics')
        self.assertEqual(vmss_ext.extension_type, 'IaaSDiagnostics')
        self.assertEqual(vmss_ext.type_handler_version, '1.9')
        self.assertTrue(vmss_ext.attached_resource_id in
                         ('/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/CR3672-RG/providers/Microsoft.Compute/virtualMachineScaleSets/cr3672-vmss',
                          'azurerm_windows_virtual_machine_scale_set.vmss.id'))
        vmss = next((vmss for vmss in ctx.virtual_machines_scale_sets if vmss.name == 'cr3672-vmss'))
        self.assertIsNotNone(vmss)
        self.assertTrue(len(vmss.extensions), 1)
        self.assertEqual(vmss.extensions[0].publisher, 'Microsoft.Azure.Diagnostics')

    @context(module_path="basic_nested_block")
    def test_basic_nested_block(self, ctx: AzureEnvironmentContext):
        vmss_ext = next((ext for ext in ctx.vms_extentions if ext.name == 'MSILinuxExtension'))
        self.assertIsNotNone(vmss_ext)
        self.assertEqual(vmss_ext.publisher, 'Microsoft.ManagedIdentity')
        self.assertEqual(vmss_ext.extension_type, 'ManagedIdentityExtensionForLinux')
        self.assertEqual(vmss_ext.type_handler_version, '1.0')
        self.assertTrue(vmss_ext.attached_resource_id in
                         ('/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/CR2340-RG/providers/Microsoft.Compute/virtualMachineScaleSets/cr2340-vmss',
                          'azurerm_virtual_machine_scale_set.vmss.id'))
        vmss = next((vmss for vmss in ctx.virtual_machines_scale_sets if vmss.name == 'cr2340-vmss'))
        self.assertIsNotNone(vmss)
        self.assertTrue(len(vmss.extensions), 1)
        self.assertEqual(vmss.extensions[0].publisher, 'Microsoft.ManagedIdentity')
