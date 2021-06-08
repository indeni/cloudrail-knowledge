from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureRedshiftClusterCreatedEncryptedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_redshift_cluster_encrypt_at_rest_creating'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for redshift_cluster in env_context.redshift_clusters:
            if redshift_cluster.is_new_resource():
                if not redshift_cluster.encrypted:
                    issues.append(
                        Issue(
                            f'The {redshift_cluster.get_type()} `{redshift_cluster.get_friendly_name()}` is not '
                            f'set to use encryption at rest', redshift_cluster, redshift_cluster))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.redshift_clusters)
