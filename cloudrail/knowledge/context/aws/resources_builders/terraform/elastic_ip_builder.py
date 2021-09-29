from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_elastic_ip
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElasticIpBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_elastic_ip(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ELASTIC_IP
