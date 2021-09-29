from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_redshift_cluster, build_redshift_subnet_group,\
    build_redshift_logging
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class RedshiftBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_redshift_cluster(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_REDSHIFT_CLUSTER


class RedshiftSubnetGroupBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_redshift_subnet_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_REDSHIFT_SUBNET_GROUP


class RedshiftLoggingBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_redshift_logging(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_REDSHIFT_CLUSTER
