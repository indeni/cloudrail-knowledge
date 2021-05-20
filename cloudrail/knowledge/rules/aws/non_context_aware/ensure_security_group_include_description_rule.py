from typing import List, Dict, Tuple
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup

from cloudrail.knowledge.context.aws.ec2.security_group_rule import SecurityGroupRule
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSecurityGroupIncludeDescriptionRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_aws_ec2_security_group_rule_no_desc'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        resources = env_context.get_all_network_entities()
        security_groups_issues = self._get_security_groups_affected_list(resources)
        for group_rule, security_group in security_groups_issues[0]:
            issues.append(
                Issue(
                    f'The {security_group.get_type()} `{security_group.get_friendly_name()}` does not '
                    f'have a description for the '
                    f'`{group_rule.get_friendly_name()}`', security_group, group_rule))
        for security_group in security_groups_issues[1]:
            issues.append(
                Issue(
                    f'The {security_group.get_type()} `{security_group.get_friendly_name()}` does not '
                    f'have a non-default description', security_group, security_group))
        return issues

    @staticmethod
    def _get_security_groups_affected_list(resources: List[NetworkEntity]) -> \
            Tuple[List[Tuple[SecurityGroupRule, SecurityGroup]], List[SecurityGroup]]:
        security_groups_without_desc = []
        security_group_rules_without_desc = []
        for resource in resources:
            network_resources = resource.network_resource
            for network_interface in network_resources.network_interfaces:
                for security_group in network_interface.security_groups:
                    if not security_group.has_description:
                        security_groups_without_desc.append(security_group)
                    for security_group_rule in security_group.inbound_permissions:
                        if not security_group_rule.has_description and security_group_rule not in security_group_rules_without_desc:
                            security_group_rules_without_desc.append((security_group_rule, security_group))
                    for security_group_rule in security_group.outbound_permissions:
                        if not security_group_rule.has_description and '0.0.0.0/0' not in security_group_rule.property_value \
                                and security_group_rule not in security_group_rules_without_desc:
                            security_group_rules_without_desc.append((security_group_rule, security_group))
        return security_group_rules_without_desc, security_groups_without_desc

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.get_all_network_entities())
