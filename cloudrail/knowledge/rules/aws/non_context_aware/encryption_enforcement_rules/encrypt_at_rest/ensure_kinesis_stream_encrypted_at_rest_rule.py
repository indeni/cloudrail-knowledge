from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureKinesisStreamEncryptedAtRestRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_kinesis_stream_encrypt_at_rest'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for kinesis_stream in env_context.kinesis_streams:
            if not kinesis_stream.encrypted_at_rest:
                issues.append(
                    Issue(
                        f'The {kinesis_stream.get_type()} `{kinesis_stream.get_friendly_name()}` '
                        f'is not set to use encryption at rest', kinesis_stream, kinesis_stream))

        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.kinesis_streams)
