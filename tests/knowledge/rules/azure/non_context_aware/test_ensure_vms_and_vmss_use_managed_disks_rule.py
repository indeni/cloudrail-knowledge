from unittest import TestCase
from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine, DiskSettings, OsDisk
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_vms_and_vmss_use_managed_disks_rule import EnsureVmAndVmssUseManagedDisksRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureVmAndVmssUseManagedDisksRule(TestCase):

    def setUp(self):
        self.rule = EnsureVmAndVmssUseManagedDisksRule()

    @parameterized.expand(
        [
            ["virtual_machine_unmanaged_disk", False, True, 'virtual_machine'],
            ["virtual_machine_managed_disk", True, False, 'virtual_machine'],
            ["vmss_unmanaged_disk", False, True, 'vmss'],
            ["vmss_managed_disk", True, False, 'vmss']
        ]
    )
    def test_auth_states(self, unused_name: str, unmanaged_disk: bool, should_alert: bool, resource_type: str):
        # Arrange
        virtual_machine: AzureVirtualMachine = create_empty_entity(AzureVirtualMachine)
        virtual_machines_scales_set: AzureVirtualMachineScaleSet = create_empty_entity(AzureVirtualMachineScaleSet)
        disk_settings: DiskSettings = create_empty_entity(DiskSettings)
        os_disk: OsDisk = create_empty_entity(OsDisk)
        os_disk.is_managed_disk = unmanaged_disk
        disk_settings.os_disk = os_disk
        virtual_machine.disk_settings = disk_settings
        virtual_machines_scales_set.disk_settings = disk_settings
        if resource_type == 'virtual_machine':
            context = AzureEnvironmentContext(virtual_machines=AliasesDict(virtual_machine))
        else:
            context = AzureEnvironmentContext(virtual_machines_scale_sets=AliasesDict(virtual_machines_scales_set))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
