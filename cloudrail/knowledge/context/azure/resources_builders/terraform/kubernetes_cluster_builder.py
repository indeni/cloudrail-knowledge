from cloudrail.knowledge.context.azure.resources.aks.azure_kubernetes_cluster import AzureKubernetesCluster
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class KubernetesClusterBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureKubernetesCluster:
        rbac = self._get_known_value(attributes, 'role_based_access_control', [{'enabled': False}])[0]
        return AzureKubernetesCluster(name=attributes['name'],
                                      enable_rbac=rbac['enabled'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_KUBERNETES_CLUSTER
