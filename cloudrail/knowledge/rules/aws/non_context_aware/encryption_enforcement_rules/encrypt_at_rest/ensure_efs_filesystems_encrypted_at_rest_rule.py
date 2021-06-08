from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureEfsFilesystemsEncryptedAtRestRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_efs_filesystem_encrypt_at_rest_creating'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for efs in env_context.efs_file_systems:
            if efs.is_new_resource() and not efs.encrypted:
                issues.append(
                    Issue(
                        f'The {efs.get_type()} `{efs.get_friendly_name()}` '
                        f'is not set to use encryption at rest', efs, efs))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.efs_file_systems)
