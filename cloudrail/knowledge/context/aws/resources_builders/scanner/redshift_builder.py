from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_redshift_cluster, \
    build_redshift_subnet_group, build_redshift_logging


class RedshiftBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'redshift-describe-clusters.json'

    def get_section_name(self) -> str:
        return 'Clusters'

    def do_build(self, attributes: dict):
        return build_redshift_cluster(attributes)


class RedshiftSubnetGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'redshift-describe-cluster-subnet-groups.json'

    def get_section_name(self) -> str:
        return 'ClusterSubnetGroups'

    def do_build(self, attributes: dict):
        return build_redshift_subnet_group(attributes)


class RedshiftLoggingBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'redshift-describe-logging-status/*'

    def get_section_name(self) -> str:
        return ''

    def do_build(self, attributes: dict):
        return build_redshift_logging(attributes)
