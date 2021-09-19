import abc
from typing import Type, Any, Dict

from cloudrail.knowledge.context.azure.azure_terraform_environment_context_builder import AzureTerraformEnvironmentContextBuilder
from cloudrail.knowledge.context.cloud_provider import CloudProvider

from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.context.environment_context.base_environment_context_builder import BaseEnvironmentContextBuilder
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory

from tests.knowledge.context.base_context_test import BaseContextTest


class AzureContextTest(BaseContextTest):
    DUMMY_ACCOUNT_ID = 'ae7905ce-4577-4a32-934b-9f662c77869d'
    DUMMY_TENANT_ID = '871cad0f-903e-4648-9655-89b796e7c99e'

    @property
    def context_builder_extra_args(self) -> Dict[str, Any]:
        return {'tenant_id': self.DUMMY_TENANT_ID}

    @property
    def cloud_provider(self):
        return CloudProvider.AZURE

    def get_provider_name(self):
        return 'azure'

    def build_context(self, base_scanner_data_for_iac, output_path):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AZURE,
                                                    IacType.TERRAFORM).build(
            base_scanner_data_for_iac,
            output_path,
            self.DUMMY_ACCOUNT_ID,
            salt=self.DUMMY_SALT,
            **self.context_builder_extra_args)

    def get_latest_provider_block(self):
        return """
provider "azurerm" {
  features {}
}
        """

    def get_version_provider_block(self, version):
        return """
provider "azurerm" {{
  features {{}}
  version = "{}"
}} 
        """.format(version)

    @abc.abstractmethod
    def get_component(self):
        pass

    def create_context_builder_factory(self) -> Type[BaseEnvironmentContextBuilder]:
        return AzureTerraformEnvironmentContextBuilder


class AzureNoCloudAccountContextTest(AzureContextTest):

    def create_context_builder_factory(self) -> Type[BaseEnvironmentContextBuilder]:
        return AzureTerraformEnvironmentContextBuilder

    def get_component(self):
        pass

    def build_context(self, base_scanner_data_for_iac, output_path):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AZURE, IacType.TERRAFORM).build(base_scanner_data_for_iac,
                                                                                                  output_path,
                                                                                                  None,
                                                                                                  self.DUMMY_SALT)
