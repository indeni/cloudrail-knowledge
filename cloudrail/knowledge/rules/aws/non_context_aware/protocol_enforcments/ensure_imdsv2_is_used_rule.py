from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureImdsv2IsUsedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ensure_imdsv2'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for ec2 in env_context.ec2s:
            if ec2.http_tokens != 'required':
                issues.append(
                    Issue(f"The {ec2.get_type()} `{ec2.get_friendly_name()}` is allowing IMDSv1", ec2, ec2)
                )

        for launch_config in env_context.launch_configurations:
            if launch_config.http_tokens != 'required':
                issues.append(
                    Issue(f"The {launch_config.get_type()} `{launch_config.get_friendly_name()}` is allowing IMDSv1", \
                          launch_config, launch_config)
                )

        for launch_template in env_context.launch_templates:
            if launch_template.http_token != 'required':
                issues.append(
                    Issue(f"The {launch_template.get_type()} `{launch_template.get_friendly_name()}` is allowing IMDSv1", \
                          launch_template, launch_template)
                )

        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ec2s or
                    environment_context.launch_templates or
                    environment_context.launch_configurations)
