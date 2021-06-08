from typing import List, Dict
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSqsQueuesEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_sqs_queues_encrypted_at_rest_with_customer_managed_cmk'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for sqs_queue in env_context.sqs_queues:
            if sqs_queue.encrypted_at_rest:
                if sqs_queue.kms_data is None or sqs_queue.kms_data.key_manager != KeyManager.CUSTOMER:
                    issues.append(
                        Issue(
                            f'The SQS queue `{sqs_queue.get_friendly_name()}` is not set '
                            f'to be encrypted at rest using customer-managed CMK', sqs_queue, sqs_queue))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.sqs_queues)
