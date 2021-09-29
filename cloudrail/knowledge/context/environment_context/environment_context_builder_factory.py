from cloudrail.knowledge.context.cloud_provider import CloudProvider

from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.exceptions import UnsupportedIacTypeException, UnsupportedCloudProviderException
from cloudrail.knowledge.context.aws.aws_cloudformation_environment_context_builder import AwsCloudformationEnvironmentContextBuilder
from cloudrail.knowledge.context.aws.aws_terraform_environment_context_builder import AwsTerraformEnvironmentContextBuilder
from cloudrail.knowledge.context.azure.azure_terraform_environment_context_builder import AzureTerraformEnvironmentContextBuilder
from cloudrail.knowledge.context.gcp.gcp_terraform_environment_context_builder import GcpTerraformEnvironmentContextBuilder


class EnvironmentContextBuilderFactory:

    @classmethod
    def get(cls, cloud_provider: CloudProvider, iac_type: IacType):
        if cloud_provider == CloudProvider.AMAZON_WEB_SERVICES:
            if iac_type == IacType.TERRAFORM:
                return AwsTerraformEnvironmentContextBuilder
            if iac_type == IacType.CLOUDFORMATION:
                return AwsCloudformationEnvironmentContextBuilder
            raise UnsupportedIacTypeException(iac_type)
        if cloud_provider == CloudProvider.AZURE:
            if iac_type == IacType.TERRAFORM:
                return AzureTerraformEnvironmentContextBuilder
            raise UnsupportedIacTypeException(iac_type)
        if cloud_provider == CloudProvider.GCP:
            if iac_type == IacType.TERRAFORM:
                return GcpTerraformEnvironmentContextBuilder
            raise UnsupportedIacTypeException(iac_type)
        raise UnsupportedCloudProviderException(cloud_provider)
