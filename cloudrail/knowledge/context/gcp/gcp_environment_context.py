from typing import List, Dict

from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext, CheckovResult
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance


class GcpEnvironmentContext(BaseEnvironmentContext):

    def __init__(self,
                 checkov_results: Dict[str, List[CheckovResult]] = None,
                 sql_database_instances: List[GcpSqlDatabaseInstance] = None,
                 compute_instances: List[GcpComputeInstance] = None,
                 compute_networks: List[GcpComputeNetwork] = None):
        BaseEnvironmentContext.__init__(self)
        self.checkov_results: Dict[str, List[CheckovResult]] = checkov_results or {}
        self.sql_database_instances: List[GcpSqlDatabaseInstance] = sql_database_instances or []
        self.compute_instances: List[GcpComputeInstance] = compute_instances or []
        self.compute_networks: List[GcpComputeNetwork] = compute_networks or []
