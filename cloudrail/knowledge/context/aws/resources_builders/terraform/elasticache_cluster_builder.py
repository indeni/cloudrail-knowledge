from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_elasticache_cluster
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElastiCacheClusterBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_elasticache_cluster(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ELASTICACHE_CLUSTER
