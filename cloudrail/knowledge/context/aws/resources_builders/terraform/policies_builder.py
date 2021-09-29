from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_s3_policy, \
    build_managed_policy, build_inline_s3_policy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class S3BucketPolicyBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_s3_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET_POLICY

class S3BucketInlinePolicyBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_inline_s3_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_S3_BUCKET



class ManagedPolicyBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_managed_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_POLICY
