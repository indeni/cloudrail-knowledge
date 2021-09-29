from typing import List, Dict
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSnsTopicEncryptedAtRestWithCustomerManagerCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_sns_topics_encrypted_at_rest_with_customer_managed_cmk'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for sns_topic in env_context.sns_topics:
            if sns_topic.encrypted_at_rest:
                if (sns_topic.kms_data is None) or (sns_topic.kms_data.key_manager != KeyManager.CUSTOMER):
                    issues.append(
                        Issue(
                            f'The {sns_topic.get_type()} `{sns_topic.get_friendly_name()}` '
                            f'is not set to use encryption at rest using customer-managed CMK', sns_topic, sns_topic))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.sns_topics)
