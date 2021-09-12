from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_elasticache_subnet_group
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElastiCacheSubnetGroupBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_elasticache_subnet_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ELASTICACHE_SUBNET_GROUP
