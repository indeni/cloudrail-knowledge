from cloudrail.knowledge.context.azure.resources.aks.azure_kubernetes_cluster import AzureKubernetesCluster

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class KubernetesClusterBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return  'aks-list.json'

    def do_build(self, attributes: dict) -> AzureKubernetesCluster:
        return AzureKubernetesCluster(name=attributes['name'],
                                      enable_rbac=attributes['properties']['enableRBAC'])
