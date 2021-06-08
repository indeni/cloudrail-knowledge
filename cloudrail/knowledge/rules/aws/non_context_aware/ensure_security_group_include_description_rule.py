from typing import List, Dict, Tuple, Set

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup

from cloudrail.knowledge.context.aws.ec2.security_group_rule import SecurityGroupRule
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSecurityGroupIncludeDescriptionRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_aws_ec2_security_group_rule_no_desc'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        security_groups_issues = self._get_security_groups_affected_list(env_context.security_groups)
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
    def _get_security_groups_affected_list(security_groups: AliasesDict[SecurityGroup]) -> \
            Tuple[Set[Tuple[SecurityGroupRule, SecurityGroup]], Set[SecurityGroup]]:
        security_groups_without_desc = set()
        security_group_rules_without_desc = set()

        for security_group in security_groups:
            if not security_group.is_used:
                continue

            if not security_group.has_description:
                security_groups_without_desc.add(security_group)

            for security_group_rule in security_group.inbound_permissions:
                if not security_group_rule.has_description:
                    security_group_rules_without_desc.add((security_group_rule, security_group))

            for security_group_rule in security_group.outbound_permissions:
                if not security_group_rule.has_description and '0.0.0.0/0' not in security_group_rule.property_value:
                    security_group_rules_without_desc.add((security_group_rule, security_group))

        return security_group_rules_without_desc, security_groups_without_desc

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.security_groups)
