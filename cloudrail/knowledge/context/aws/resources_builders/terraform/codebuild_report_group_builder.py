from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_code_build_report_group
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CodeBuildReportGroupBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_code_build_report_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CODEBUILD_REPORT_GROUP
