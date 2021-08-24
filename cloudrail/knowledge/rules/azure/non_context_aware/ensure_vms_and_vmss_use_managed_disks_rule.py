from typing import Dict, List, Union

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.vm.azure_virtual_machine import AzureVirtualMachine
from cloudrail.knowledge.context.azure.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureVmAndVmssUseManagedDisksRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_virtual_machines_and_virtual_machine_scale_sets_only_use_managed_disks'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for virtual_machine in env_context.virtual_machines:
            if not virtual_machine.disk_settings.os_disk.is_managed_disk:
                self._append_issue(virtual_machine, issues)
        for vmss in env_context.virtual_machines_scale_sets:
            if not vmss.disk_settings.os_disk.is_managed_disk:
                self._append_issue(vmss, issues)
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.virtual_machines or environment_context.virtual_machines_scale_sets)

    @staticmethod
    def _append_issue(vm_entity: Union[AzureVirtualMachine, AzureVirtualMachineScaleSet], issues_list: List[Issue]):
        issues_list.append(
            Issue(
                f"The {vm_entity.get_type()} `{vm_entity.get_friendly_name()}` is using an unmanaged disk",
                vm_entity, vm_entity))
