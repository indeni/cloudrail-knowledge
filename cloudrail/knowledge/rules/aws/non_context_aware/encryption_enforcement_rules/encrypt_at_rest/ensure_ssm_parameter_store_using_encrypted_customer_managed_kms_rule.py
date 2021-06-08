from typing import List, Dict
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ssm_parameter_store_securestring_encrypted_at_rest_with_customer_managed_CMK'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for ssm_param in env_context.ssm_parameters:
            if ssm_param.kms_data is None or ssm_param.kms_data.key_manager != KeyManager.CUSTOMER:
                issues.append(
                    Issue(
                        f'The {ssm_param.get_type()} Store parameter `{ssm_param.get_friendly_name()}` is not '
                        f'encrypted at rest using customer-managed CMK', ssm_param, ssm_param))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ssm_parameters)
