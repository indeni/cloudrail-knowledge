from abc import abstractmethod
from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class SampleCustomRule(AwsBaseRule):
    @abstractmethod
    def get_id(self) -> str:
        return 'my_sample_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues = []
        for entity in env_context.vpcs:
            issues.append(
                Issue(
                    f"Vpc exists `{entity.get_friendly_name()}`", entity, entity))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return True
