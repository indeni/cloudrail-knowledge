from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class SqlDatabaseRestrictTrustedIpRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_cloud_sql_restrict_trusted_ip'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for sql_db_instance in env_context.sql_database_instances:
            if any(authorized_network.value == '0.0.0.0/0' for authorized_network in sql_db_instance.settings.ip_configuration.authorized_networks):
                issues.append(
                    Issue(
                        f'The google cloud database instance `{sql_db_instance.name}` is reachable from internet on sql port 3306.',
                        sql_db_instance,
                        sql_db_instance))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.sql_database_instances)
