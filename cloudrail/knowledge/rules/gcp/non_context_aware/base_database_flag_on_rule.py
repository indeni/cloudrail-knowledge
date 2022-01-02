from abc import abstractmethod
from typing import Dict, List
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class BaseDatabaseFlagOnRule(GcpBaseRule):

    @abstractmethod
    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    @staticmethod
    def is_version_contains(db_instance: GcpSqlDatabaseInstance, version_prefix: str):
        return db_instance.database_version and version_prefix in db_instance.database_version.value

    @classmethod
    def is_flag_on(cls, db_instance: GcpSqlDatabaseInstance, flag_name: str) -> bool:
        return cls.is_flag_mode(db_instance, flag_name, 'on')

    @classmethod
    def is_flag_off(cls, db_instance: GcpSqlDatabaseInstance, flag_name: str) -> bool:
        return cls.is_flag_mode(db_instance, flag_name, 'off')

    @staticmethod
    def is_flag_mode(db_instance: GcpSqlDatabaseInstance, flag_name: str, *flag_mode: str) -> bool:
        return db_instance.settings is not None and \
               db_instance.settings.database_flags is not None and \
               any(db_flag.name == flag_name and db_flag.value in flag_mode
                   for db_flag in db_instance.settings.database_flags)

    @abstractmethod
    def get_id(self) -> str:
        pass

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.sql_database_instances)
