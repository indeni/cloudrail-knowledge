from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSnsTopicEncryptedAtRestRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_sns_topic_encrypt_at_rest'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for sns_topic in env_context.sns_topics:
            if not sns_topic.encrypted_at_rest:
                issues.append(
                    Issue(
                        f'The {sns_topic.get_type()} `{sns_topic.get_friendly_name()}` '
                        f'is not set to use encryption at rest', sns_topic, sns_topic))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.sns_topics)
