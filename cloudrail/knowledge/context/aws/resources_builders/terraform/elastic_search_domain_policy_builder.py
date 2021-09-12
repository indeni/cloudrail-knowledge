from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_elastic_search_domain_policy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElasticSearchDomainPolicyBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_elastic_search_domain_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ELASTICSEARCH_DOMAIN_POLICY
