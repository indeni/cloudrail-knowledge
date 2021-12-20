from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet
from cloudrail.knowledge.utils.utils import create_pseudo_id


class PseudoBuilder:
    def __init__(self, azure_ctx: AzureEnvironmentContext):
        self.ctx = azure_ctx

    def create_vm_from_vmss(self, vmss_list: AliasesDict[AzureVirtualMachineScaleSet]):
        vm_num = 0
        for vmss in vmss_list:
            network_interface_ids = []
            for network_interface in vmss.network_interfaces_config:
                network_interface_ids.append(create_pseudo_id(network_interface.name))
            vm_name = f'{vmss.name}_{vm_num}_f{create_pseudo_id(vmss.name)}'
            vm_num += 1
            azure_virtual_machine = AzureVirtualMachine(vm_name, network_interface_ids, vmss.os_type, vmss.disk_settings)
            azure_virtual_machine.is_pseudo = True
            self.ctx.virtual_machines.update(azure_virtual_machine)
