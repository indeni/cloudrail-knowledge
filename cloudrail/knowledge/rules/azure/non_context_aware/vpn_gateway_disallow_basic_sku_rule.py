from typing import Dict, List

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.network.azure_vnet_gateway import VirtualNetworkGatewayType
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class VpnGatewayDisallowBasicSkuRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_vpn_gateway_disallow_basic_sku'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for vnet_gw in env_context.vnet_gateways:
            if vnet_gw.gateway_type == VirtualNetworkGatewayType.VPN and vnet_gw.sku_tier == 'Basic':
                issues.append(
                    Issue(
                        f'{vnet_gw.get_type()} `{vnet_gw.get_friendly_name()}` uses "basic" SKU',
                        vnet_gw,
                        vnet_gw))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.vnet_gateways)
