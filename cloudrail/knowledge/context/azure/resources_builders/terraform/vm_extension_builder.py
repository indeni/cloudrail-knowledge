from typing import List, Optional
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine_extension import AzureVirtualMachineExtension, ResourceType
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class VmssBasicExtensionBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureVirtualMachineExtension:
        attributes['resource_type'] = 'vmss'
        attributes['attached_resource_id'] = attributes['virtual_machine_scale_set_id']
        return _build_vm_extension(attributes)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_MACHINE_SCALE_SET_EXTENSION


class VmssNestedExtensionBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> Optional[List[AzureVirtualMachineExtension]]:
        vmss_extensions = []
        for extension_attributes in self._get_known_value(attributes, 'extension', []):
            extension_attributes['attached_resource_id'] = attributes['id']
            extension_attributes['resource_type'] = 'vmss'
            vmss_extensions.append(_build_vm_extension(extension_attributes))
        return vmss_extensions

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_MACHINE_SCALE_SET


class VmExtensionBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> Optional[List[AzureVirtualMachineExtension]]:
        attributes['resource_type'] = 'vm'
        attributes['attached_resource_id'] = attributes['virtual_machine_id']
        return _build_vm_extension(attributes)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_MACHINE_EXTENSION


def _build_vm_extension(attributes: dict) -> AzureVirtualMachineExtension:
    return AzureVirtualMachineExtension(name=attributes['name'],
                                        publisher=attributes['publisher'],
                                        extension_type=attributes['type'],
                                        type_handler_version=attributes['type_handler_version'],
                                        attached_resource_id=attributes['attached_resource_id'],
                                        resource_attached_type=ResourceType(attributes['resource_type']))
