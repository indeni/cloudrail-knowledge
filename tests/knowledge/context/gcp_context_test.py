import abc
from typing import Type

from cloudrail.knowledge.context.cloud_provider import CloudProvider

from cloudrail.knowledge.context.iac_type import IacType 
from cloudrail.knowledge.context.environment_context.base_environment_context_builder import BaseEnvironmentContextBuilder
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from cloudrail.knowledge.context.gcp.gcp_terraform_environment_context_builder import GcpTerraformEnvironmentContextBuilder

from test.knowledge.context.base_context_test import BaseContextTest


class GcpContextTest(BaseContextTest):
    DUMMY_ACCOUNT_ID = 'dev-test'

    @property
    def cloud_provider(self):
        return CloudProvider.GCP

    def get_provider_name(self):
        return 'gcp'

    def build_context(self, base_scanner_data_for_iac, output_path):
        return EnvironmentContextBuilderFactory.get(CloudProvider.GCP, IacType.TERRAFORM).build(base_scanner_data_for_iac,
                                                                                                output_path,
                                                                                                self.DUMMY_ACCOUNT_ID,
                                                                                                self.DUMMY_SALT)

    def get_latest_provider_block(self):
        return """
provider "google" {
}
        """

    def get_version_provider_block(self, version):
        return """
terraform {{
  required_providers {{
    google = {{
      source = "hashicorp/google"
      version = "{0}"
    }}
  }}
}}

provider "google" {{
}}
        """.format(version)

    @abc.abstractmethod
    def get_component(self):
        pass

    def create_context_builder_factory(self) -> Type[BaseEnvironmentContextBuilder]:
        return GcpTerraformEnvironmentContextBuilder


class GcpNoCloudAccountContextTest(GcpContextTest):

    def create_context_builder_factory(self) -> Type[BaseEnvironmentContextBuilder]:
        return GcpTerraformEnvironmentContextBuilder

    def get_component(self):
        pass

    def build_context(self, base_scanner_data_for_iac, output_path):
        return EnvironmentContextBuilderFactory.get(CloudProvider.GCP, IacType.TERRAFORM).build(base_scanner_data_for_iac,
                                                                                                output_path,
                                                                                                None,
                                                                                                self.DUMMY_SALT)
