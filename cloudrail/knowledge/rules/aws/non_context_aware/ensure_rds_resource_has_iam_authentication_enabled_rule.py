from typing import List, Dict, Union

from cloudrail.knowledge.context.aws.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureRdsResourceIamAuthenticationEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_rds_database_iam_authentication_enabled'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        rds_resources = env_context.rds_clusters + env_context.rds_instances
        for resource in rds_resources:
            if self._version_rds_check(resource) and not resource.iam_database_authentication_enabled:
                issues.append(
                    Issue(
                        f'The {resource.get_type()} `{resource.get_friendly_name()}` does not have a backup retention policy configured', resource, resource))
            return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.rds_clusters or environment_context.rds_instances)

    @staticmethod
    def _version_rds_check(rds_resource: Union[RdsCluster, RdsInstance]) -> bool:
        supported_mysql_versions = ['5.6.34', '5.7.16', '8.0.16']
        supported_postgres_versions = ['9.5.15', '9.6.11', '10.6', '11', '12', '13']
        if isinstance(rds_resource, RdsInstance):
            if rds_resource.engine_type.lower() == 'mysql':


