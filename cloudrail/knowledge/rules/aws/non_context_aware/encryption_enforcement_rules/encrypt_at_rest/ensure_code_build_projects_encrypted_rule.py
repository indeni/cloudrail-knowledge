from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCodeBuildProjectsEncryptedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'not_car_codebuild_projects_encrypted_at_rest_with_customer_managed_CMK'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for project in env_context.codebuild_projects:
            if not project.kms_data or project.kms_data.key_manager != KeyManager.CUSTOMER:
                issues.append(
                    Issue(
                        f'The {project.get_type()} project `{project.get_friendly_name()}` '
                        f'is not set to use encryption at rest '
                        f'with customer-managed CMK', project, project))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.codebuild_projects)
