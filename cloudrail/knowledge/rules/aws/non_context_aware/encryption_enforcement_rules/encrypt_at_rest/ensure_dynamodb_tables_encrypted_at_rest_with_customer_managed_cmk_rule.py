from typing import List, Dict
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_dynamodb_tables_encrypted_at_rest_with_customer_managed_CMK'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for table in env_context.dynamodb_table_list:
            if not table.server_side_encryption or table.kms_data.key_manager != KeyManager.CUSTOMER:
                issues.append(
                    Issue(
                        f'The {table.get_type()} `{table.get_friendly_name()}` '
                        f'is not set to be encrypted at rest using customer-managed CMK', table, table))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.dynamodb_table_list)
