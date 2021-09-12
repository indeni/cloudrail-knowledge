from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ecr_repositories_encrypted_at_rest_with_customer_managed_cmk'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for ecr in env_context.ecr_repositories:
            if ecr.is_new_resource():
                if ecr.encryption_type != 'KMS' or (ecr.encryption_type == 'KMS' and ecr.kms_data.key_manager != KeyManager.CUSTOMER):
                    issues.append(
                        Issue(
                            f'The {ecr.get_type()} `{ecr.get_friendly_name()}` '
                            f'is not set to be encrypted at rest using customer-managed CMK', ecr, ecr))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ecr_repositories)
