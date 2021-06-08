from typing import Dict, List

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureNoUnusedSecurityGroups(BaseRule):

    def get_id(self) -> str:
        return 'car_unused_security_group'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        # Currently, we catch only security groups which are exists, and not ones which are being created.
        # This is in order to avoid scenario in which a security group created, and will be associated using a different infra than TF.
        # In the future, we will add history track for resources, and this condition will not be needed.
        for security_group in [sg for sg in env_context.security_groups if
                               not sg.is_used
                               and not sg.is_new_resource()
                               and not sg.is_pseudo]:
            issues.append(
                Issue(
                    f'The {security_group.get_type()} `{security_group.get_friendly_name()}` is not used by any AWS resource'
                    , security_group, security_group))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.security_groups and environment_context.network_interfaces)
