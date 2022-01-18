from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer_probe import AzureLoadBalancerProbe, AzureLoadBalancerProbeProtocol
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class LoadBalancerProbeBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureLoadBalancerProbe:
        return AzureLoadBalancerProbe(name=attributes['name'],
                                      loadbalancer_id=attributes['loadbalancer_id'],
                                      protocol=enum_implementation(AzureLoadBalancerProbeProtocol, self._get_known_value(attributes, 'protocol', 'Tcp')),
                                      port=attributes['port'],
                                      request_path=self._get_known_value(attributes, 'request_path'),
                                      interval_in_seconds=self._get_known_value(attributes, 'interval_in_seconds', 15),
                                      number_of_probes=self._get_known_value(attributes, 'number_of_probes', 2))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_LB_PROBE
