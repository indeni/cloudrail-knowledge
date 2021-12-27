from unittest import TestCase
from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine_extension import AzureVirtualMachineExtension
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet, OperatingSystemType
from cloudrail.knowledge.rules.azure.context_aware.vmss_diagnostics_logs_enabled_rule import VmssDiagnosticsLogsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestVmssDiagnosticsLogsEnabledRule(TestCase):

    def setUp(self):
        self.rule = VmssDiagnosticsLogsEnabledRule()

    @parameterized.expand(
        [
            ["no_logs_enabled_windows", OperatingSystemType.WINDOWS,
             'Microsoft.Azure.Applications', 'IaaS47C6E03DTest', True],
            ["logs_enabled_windows", OperatingSystemType.WINDOWS,
             'Microsoft.Azure.Diagnostics', 'IaaSDiagnostics', False],
            ["no_logs_enabled_linux", OperatingSystemType.LINUX,
             'Microsoft.HpcPack', 'LinuxNodeAgent', True],
            ["logs_enabled_linux", OperatingSystemType.LINUX,
             'Microsoft.OSTCExtensions', 'LinuxDiagnostic', False]
        ]
    )
    def test_vmss_diagnostics_logs(self, unused_name: str, os_type: OperatingSystemType, publisher: str,
                                   extension_type: str, should_alert: bool):
        # Arrange
        virtual_machines_scales_set: AzureVirtualMachineScaleSet = create_empty_entity(AzureVirtualMachineScaleSet)
        virtual_machines_scales_set.name = 'vmss-test'
        virtual_machines_scales_set.os_type = os_type
        vmss_extension: AzureVirtualMachineExtension = create_empty_entity(AzureVirtualMachineExtension)
        vmss_extension.publisher = publisher
        vmss_extension.extension_type = extension_type
        virtual_machines_scales_set.extensions.append(vmss_extension)
        context = AzureEnvironmentContext(virtual_machines_scale_sets=AliasesDict(virtual_machines_scales_set),
                                          vms_extentions=AliasesDict(vmss_extension))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
