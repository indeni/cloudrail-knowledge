from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_iam_policy_attachment
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class IamPolicyAttachmentBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_policy_attachment(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_POLICY_ATTACHMENT
