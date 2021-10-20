from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class SqlDatabaseSslRequiredRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_gcp_sql_database_ssl_required'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for sql_db_instance in env_context.sql_database_instances:
            if settings := sql_db_instance.settings:
                if ip_configuration := settings.ip_configuration:
                    if not ip_configuration.require_ssl:
                        # TODO: Fix evidence
                        issues.append(
                            Issue(
                                f'~{sql_db_instance.get_type()}~. '
                                f'The {sql_db_instance.get_type()} `{sql_db_instance.get_friendly_name()}` is not requiring SSL',
                                sql_db_instance,
                                sql_db_instance))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.sql_database_instances)
