from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureWorkspaceUserVolumeEncryptedAtRestRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_workspace_user_volume_encrypt_at_rest_creating'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for workspace in env_context.workspaces:
            if workspace.is_new_resource() and not workspace.user_encryption_enabled:
                issues.append(
                    Issue(
                        f'The {workspace.get_type()} `{workspace.get_friendly_name()}` '
                        f'is not set to encrypt user volume at rest', workspace, workspace))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.workspaces)
