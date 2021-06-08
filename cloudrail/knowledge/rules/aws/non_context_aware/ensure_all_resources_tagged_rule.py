from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureAllResourcesTaggedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_all_resources_tagged'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for resource in env_context.get_all_taggable_resources():
            if resource.tags and all(tag in ('name', 'Name') for tag in resource.tags.keys()):
                issues.append(
                    Issue(
                        f'Resource {resource.get_type()} `{resource.get_friendly_name()}` does not have any tags set other than "Name"',
                        resource, resource))
            elif not resource.tags:
                issues.append(
                    Issue(
                        f'Resource {resource.get_type()} `{resource.get_friendly_name()}` does not have any tags set', resource, resource))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.get_all_taggable_resources())
