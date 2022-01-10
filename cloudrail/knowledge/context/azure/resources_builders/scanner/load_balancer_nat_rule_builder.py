from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer_nat_rule import AzureLoadBalancerNatRule, AzureLoadBalancerNatRuleProtocol
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class LoadBalancerNatRuleBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-load-balancer-inbound-nat-rules.json'

    def do_build(self, attributes: dict) -> AzureLoadBalancerNatRule:
        properties = attributes['properties']
        return AzureLoadBalancerNatRule(name=attributes['name'],
                                        loadbalancer_id=attributes['id'].split('/inboundNatRules')[0],
                                        frontend_ip_configuration_name=properties['frontendIPConfiguration']['id'].split('frontendIPConfigurations/')[-1],
                                        protocol=enum_implementation(AzureLoadBalancerNatRuleProtocol, properties['protocol'].lower()),
                                        frontend_port=properties['frontendPort'],
                                        backend_port=properties['backendPort'],
                                        idle_timeout_in_minutes=properties['idleTimeoutInMinutes'],
                                        enable_floating_ip=properties['enableFloatingIP'],
                                        enable_tcp_reset=properties['enableTcpReset'])
