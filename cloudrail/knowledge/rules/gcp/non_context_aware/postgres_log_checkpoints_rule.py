from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.non_context_aware.base_database_flag_on_rule import BaseDatabaseFlagOnRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PostgresLogCheckpointsRule(BaseDatabaseFlagOnRule):

    def get_id(self) -> str:
        return 'non_car_cloud_sql_log_checkpoints_on'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for sql_db in env_context.sql_database_instances:
            if self.is_version_contains(sql_db, 'POSTGRES') and \
                    self.is_flag_off(sql_db, 'log_checkpoints'):
                issues.append(
                    Issue(
                        f"The Google Cloud {sql_db.get_type()} `{sql_db.get_friendly_name()}` has database"
                        f" flag `log_checkpoints` set to off.",
                        sql_db,
                        sql_db))
        return issues
