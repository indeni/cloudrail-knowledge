from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureDaxClustersEncryptedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'not_car_dynamodb_dax_clusters_encrypted_at_rest'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for dax_cluster in env_context.dax_cluster:
            if dax_cluster.is_new_resource():
                if not dax_cluster.server_side_encryption:
                    issues.append(
                        Issue(
                            f'The {dax_cluster.get_type()} `{dax_cluster.get_friendly_name()}` is not set '
                            f'to be encrypted at rest', dax_cluster, dax_cluster))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.dax_cluster)
