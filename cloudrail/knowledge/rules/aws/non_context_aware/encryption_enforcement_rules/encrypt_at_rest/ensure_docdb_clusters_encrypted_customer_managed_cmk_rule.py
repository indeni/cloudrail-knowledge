from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureDocdbClustersEncryptedCustomerManagedCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'not_car_docdb_cluster_encrypted_at_rest_using_customer_managed_cmk'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for docdb_cluster in env_context.docdb_cluster:
            if docdb_cluster.is_new_resource() and docdb_cluster.storage_encrypted:
                if not docdb_cluster.kms_data or docdb_cluster.kms_data.key_manager != KeyManager.CUSTOMER:
                    issues.append(
                        Issue(
                            f'The DocDB cluster `{docdb_cluster.get_friendly_name()}` is not set '
                            f'to be encrypted at rest using customer-managed CMK', docdb_cluster, docdb_cluster))

        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.docdb_cluster)
