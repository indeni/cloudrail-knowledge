from typing import List, Dict
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureWorkspaceRootVolumeEncryptionCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_workspace_root_volume_encrypt_at_rest_with_customer_managed_CMK_creating'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for workspace in env_context.workspaces:
            if workspace.is_new_resource():
                if workspace.root_encryption_enabled and workspace.keys_data and \
                        workspace.keys_data.key_manager != KeyManager.CUSTOMER:
                    issues.append(
                        Issue(f'The {workspace.get_type()} `{workspace.get_friendly_name()}` is '
                              f'not set to encrypt root volume at rest using customer-managed CMK',
                              workspace, workspace))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.workspaces)
