from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_neptune_cluster, build_neptune_instance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class NeptuneClusterBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_neptune_cluster(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_NEPTUNE_CLUSTER


class NeptuneInstanceBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_neptune_instance(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_NEPTUNE_CLUSTER_INSTANCE
