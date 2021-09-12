from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_rds_cluster_instance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class RdsClusterInstanceBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_rds_cluster_instance(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_RDS_CLUSTER_INSTANCE
