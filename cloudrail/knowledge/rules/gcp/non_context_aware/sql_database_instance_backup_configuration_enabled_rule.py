from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class SqlDatabaseBackupConfigurationEnabledRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_cloud_sql_enable_backup'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for sql_db_instance in env_context.sql_database_instances:
            if sql_db_instance.settings and not sql_db_instance.settings.backup_configuration.enabled:
                issues.append(
                    Issue(
                        f"The Google Cloud {sql_db_instance.get_type()} `{sql_db_instance.get_friendly_name()}` has backup_configured enabled flag not set.",
                        sql_db_instance,
                        sql_db_instance))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.sql_database_instances)
