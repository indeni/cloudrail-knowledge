from typing import List, Dict
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureXrayEncryptionCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_xray_encryption_config_encrypt_at_rest_with_customer_managed_CMK'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for xray in env_context.xray_encryption_configurations:
            if xray.kms_data is None or (xray.key_id and xray.kms_data.key_manager != KeyManager.CUSTOMER) \
                 or not xray.key_id:
                issues.append(
                    Issue(f'The {xray.get_type()} config is not set to encrypt at rest using customer-managed CMK',
                          xray, xray))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.xray_encryption_configurations)
