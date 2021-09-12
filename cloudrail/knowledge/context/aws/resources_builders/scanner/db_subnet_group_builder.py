from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_db_subnet_group


class DbSubnetGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'rds-describe-db-subnet-groups.json'

    def get_section_name(self) -> str:
        return 'DBSubnetGroups'

    def do_build(self, attributes: dict):
        return build_db_subnet_group(attributes)
