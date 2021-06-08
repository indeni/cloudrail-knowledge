from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureEcrRepositoryImageTagsImmutableRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ecr_image_tags_immutable'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for ecr in env_context.ecr_repositories:
            if ecr.image_tag_mutability != 'IMMUTABLE':
                issues.append(
                    Issue(
                        f'The {ecr.get_type()} `{ecr.get_friendly_name()}` is not configured for image tag immutability', ecr, ecr))
            return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ecr_repositories)
