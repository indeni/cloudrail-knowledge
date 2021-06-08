from typing import List, Dict
from cloudrail.knowledge.context.aws.kms.kms_key import KeyManager

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_rds_cluster_instance_encrypt_performance_insights_with_customer_managed_cmk_creating'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for rds_instance in env_context.rds_instances:
            if rds_instance.is_new_resource() and rds_instance.performance_insights_enabled:
                if not rds_instance.performance_insights_kms_data or rds_instance.performance_insights_kms_data.key_manager != KeyManager.CUSTOMER:
                    issues.append(
                        Issue(
                            f'The RDS cluster instance ```{rds_instance.get_friendly_name()}``` '
                            f'is not set to be encrypted at rest using customer-managed CMK', rds_instance, rds_instance))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.rds_instances)
