from typing import Dict, List

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class UnusedNetworkSecurityGroupRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_unused_network_security_group'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for nsg in env_context.net_security_groups:
            if not nsg.subnets and not nsg.network_interfaces:
                issues.append(
                    Issue(
                        f'{nsg.get_type()}  `{nsg.get_friendly_name()}` is unused',
                        nsg,
                        nsg))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.net_security_groups)
