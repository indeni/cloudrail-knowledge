from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer_nat_rule import AzureLoadBalancerNatRule, AzureLoadBalancerNatRuleProtocol
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class LoadBalancerNatRuleBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureLoadBalancerNatRule:
        return AzureLoadBalancerNatRule(name=attributes['name'],
                                        loadbalancer_id=attributes['loadbalancer_id'],
                                        frontend_ip_configuration_name=attributes['frontend_ip_configuration_name'],
                                        protocol=enum_implementation(AzureLoadBalancerNatRuleProtocol, attributes['protocol'].lower()),
                                        frontend_port=attributes['frontend_port'],
                                        backend_port=attributes['backend_port'],
                                        idle_timeout_in_minutes=self._get_known_value(attributes, 'idle_timeout_in_minutes', 4),
                                        enable_floating_ip=self._get_known_value(attributes, 'enable_floating_ip', False),
                                        enable_tcp_reset=self._get_known_value(attributes, 'enable_tcp_reset', False))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_LB_NAT_RULE
