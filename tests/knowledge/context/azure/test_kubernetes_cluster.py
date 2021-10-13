from cloudrail.knowledge.context.azure.resources.aks.azure_kubernetes_cluster import AzureKubernetesCluster
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from test.knowledge.context.azure_context_test import AzureContextTest
from test.knowledge.context.test_context_annotation import context


class TestKubernetesCluster(AzureContextTest):

    def get_component(self):
        return "kubernetes_cluster"

    @context(module_path="kubernetes_rbac_disabled")
    def test_kubernetes_rbac_disabled(self, ctx: AzureEnvironmentContext):
        kubernetes_cluster = self._get_kubernetes_cluster(ctx)
        self.assertFalse(kubernetes_cluster.enable_rbac)

    @context(module_path="kubernetes_rbac_enabled")
    def test_kubernetes_rbac_enabled(self, ctx: AzureEnvironmentContext):
        kubernetes_cluster = self._get_kubernetes_cluster(ctx)
        self.assertTrue(kubernetes_cluster.enable_rbac)

    @context(module_path="kubernetes_rbac_not_specified")
    def test_kubernetes_rbac_not_specified(self, ctx: AzureEnvironmentContext):
        kubernetes_cluster = self._get_kubernetes_cluster(ctx)
        self.assertFalse(kubernetes_cluster.enable_rbac)

    def _get_kubernetes_cluster(self, ctx: AzureEnvironmentContext) -> AzureKubernetesCluster:
        kubernetes_cluster = next((cluster for cluster in ctx.kubernetes_cluster if cluster.name == 'cr2304aks-aks'), None)
        self.assertIsNotNone(kubernetes_cluster)
        return kubernetes_cluster
