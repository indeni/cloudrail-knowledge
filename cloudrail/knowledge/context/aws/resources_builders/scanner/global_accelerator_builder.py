from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_global_accelerator, build_global_accelerator_listener, \
    build_global_accelerator_endpoint_group, build_global_accelerator_attribute


class GlobalAcceleratorBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'globalaccelerator-list-accelerators.json'

    def get_section_name(self) -> str:
        return 'Accelerators'

    def do_build(self, attributes: dict):
        return build_global_accelerator(attributes)


class GlobalAcceleratorListenerBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'globalaccelerator-list-listeners/*'

    def get_section_name(self) -> str:
        return 'Listeners'

    def do_build(self, attributes: dict):
        return build_global_accelerator_listener(attributes)


class GlobalAcceleratorEndpointGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'globalaccelerator-list-endpoint-groups/*'

    def get_section_name(self) -> str:
        return 'EndpointGroups'

    def do_build(self, attributes: dict):
        return build_global_accelerator_endpoint_group(attributes)


class GlobalAcceleratorAttributeBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'globalaccelerator-describe-accelerator-attributes/*'

    def get_section_name(self) -> str:
        return 'AcceleratorAttributes'

    def do_build(self, attributes: dict):
        return build_global_accelerator_attribute(attributes)
