from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_cloud_watch_event_target


class CloudWatchEventTargetBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'events-list-targets-by-rule/*'

    def get_section_name(self) -> str:
        return 'Targets'

    def do_build(self, attributes: dict):
        return build_cloud_watch_event_target(attributes)
