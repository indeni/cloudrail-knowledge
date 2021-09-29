from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_dms_replication_instance, \
    build_dms_replication_instance_subnet_group


class DmsReplicationInstanceBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'dms-describe-replication-instances.json'

    def get_section_name(self) -> str:
        return 'ReplicationInstances'

    def do_build(self, attributes: dict):
        return build_dms_replication_instance(attributes)


class DmsReplicationInstanceSubnetGroupsBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'dms-describe-replication-subnet-groups.json'

    def get_section_name(self) -> str:
        return 'ReplicationSubnetGroups'

    def do_build(self, attributes: dict):
        return build_dms_replication_instance_subnet_group(attributes)
