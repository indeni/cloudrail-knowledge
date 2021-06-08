from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'ensure_all_used_default_security_groups_restrict_all_traffic_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        default_security_group_to_issues: Dict[str, Issue] = {}
        resources = env_context.get_all_network_entities()
        for resource in resources:
            network_resources = resource.network_resource
            for network_interface in network_resources.network_interfaces:
                for security_group in network_interface.security_groups:
                    if security_group.security_group_id not in default_security_group_to_issues and \
                            security_group.is_default and (len(security_group.inbound_permissions) > 0 or
                                                           len(security_group.outbound_permissions) > 0):
                        default_security_group_to_issues[security_group.security_group_id] = \
                            Issue(
                                f'~{security_group.vpc.get_type()} `{security_group.vpc.get_friendly_name()}`~. '
                                f'`{resource.get_friendly_name()}` uses '
                                f'{network_interface.get_type()} `{network_interface.get_friendly_name()}`.'
                                f' The {network_interface.get_type()} is secured by default {security_group.get_type()} '
                                f'`{security_group.get_friendly_name()}` and allows all traffic',
                                network_interface.owner,
                                security_group)

        return list(default_security_group_to_issues.values())

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.vpcs)
