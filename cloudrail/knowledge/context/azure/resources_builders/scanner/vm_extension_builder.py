from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine_extension import AzureVirtualMachineExtension, ResourceType


class VmssExtensionBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'vmss-extensions.json'

    def do_build(self, attributes: dict) -> AzureVirtualMachineExtension:
        attributes['resource_type'] = 'vmss'
        return _build_vm_extension(attributes)


class VmExtensionBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'vm-extensions.json'

    def do_build(self, attributes: dict) -> AzureVirtualMachineExtension:
        attributes['resource_type'] = 'vm'
        return _build_vm_extension(attributes)


def _build_vm_extension(attributes: dict) -> AzureVirtualMachineExtension:
    properties = attributes['properties']
    attached_resource_id = attributes['id'].split('extensions')[0][:-1]
    return AzureVirtualMachineExtension(name=attributes['name'],
                                        publisher=properties['publisher'],
                                        extension_type=properties['type'],
                                        type_handler_version=properties['typeHandlerVersion'],
                                        attached_resource_id=attached_resource_id,
                                        resource_attached_type=ResourceType(attributes['resource_type']))
