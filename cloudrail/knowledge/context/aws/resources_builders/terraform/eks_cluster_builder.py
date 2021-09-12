from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_eks_cluster
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class EksClusterBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_eks_cluster(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_EKS_CLUSTER
