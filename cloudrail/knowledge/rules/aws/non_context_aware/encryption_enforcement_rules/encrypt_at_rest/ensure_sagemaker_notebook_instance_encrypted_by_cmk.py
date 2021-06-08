from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'not_car_sagemaker_notebook_instances_encrypt_artifacts_at_rest_with_customer_managed_CMK_creating'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for notebook_instance in env_context.sagemaker_notebook_instances:
            if notebook_instance.is_new_resource() and notebook_instance.kms_data.key_manager != KeyManager.CUSTOMER:
                issues.append(
                    Issue(
                        f'The {notebook_instance.get_type()} `{notebook_instance.get_friendly_name()}` is not set '
                        f'to encrypt artifacts at rest using a customer-managed CMK', notebook_instance, notebook_instance))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.sagemaker_notebook_instances)
