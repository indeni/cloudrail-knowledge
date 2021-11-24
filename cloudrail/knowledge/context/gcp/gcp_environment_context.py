import functools
from typing import Callable, List, Dict, Set
from cloudrail.knowledge.context.aliases_dict import AliasesDict

from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext, CheckovResult
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_global_forwarding_rule import \
    GcpComputeGlobalForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_forwarding_rule import GcpComputeForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_ssl_policy import GcpComputeSslPolicy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_http_proxy import GcpComputeTargetHttpProxy
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_pool import GcpComputeTargetPool
from cloudrail.knowledge.context.gcp.resources.projects.gcp_project import Project
from cloudrail.knowledge.context.gcp.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket import GcpStorageBucket


class GcpEnvironmentContext(BaseEnvironmentContext):

    def __init__(self,
                 checkov_results: Dict[str, List[CheckovResult]] = None,
                 sql_database_instances: List[GcpSqlDatabaseInstance] = None,
                 compute_instances: List[GcpComputeInstance] = None,
                 compute_firewalls: List[GcpComputeFirewall] = None,
                 compute_networks: List[GcpComputeNetwork] = None,
                 projects: AliasesDict[Project] = None,
                 container_cluster: List[GcpContainerCluster] = None,
                 compute_target_http_proxy: List[GcpComputeTargetHttpProxy] = None,
                 compute_global_forwarding_rule: List[GcpComputeGlobalForwardingRule] = None,
                 compute_target_pools: List[GcpComputeTargetPool] = None,
                 compute_forwarding_rules: List[GcpComputeForwardingRule] = None,
                 compute_ssl_policy: List[GcpComputeSslPolicy] = None,
                 storage_buckets: AliasesDict[GcpStorageBucket] = None):
        BaseEnvironmentContext.__init__(self)
        self.checkov_results: Dict[str, List[CheckovResult]] = checkov_results or {}
        self.sql_database_instances: List[GcpSqlDatabaseInstance] = sql_database_instances or []
        self.compute_instances: List[GcpComputeInstance] = compute_instances or []
        self.compute_firewalls: List[GcpComputeFirewall] = compute_firewalls or []
        self.compute_networks: List[GcpComputeNetwork] = compute_networks or []
        self.compute_global_forwarding_rule: List[GcpComputeGlobalForwardingRule] = compute_global_forwarding_rule or []
        self.projects: AliasesDict[Project] = projects or AliasesDict()
        self.container_cluster: List[GcpContainerCluster] = container_cluster or []
        self.compute_target_http_proxy: List[GcpComputeTargetHttpProxy] = compute_target_http_proxy or []
        self.compute_target_pools: List[GcpComputeTargetPool] = compute_target_pools or []
        self.compute_forwarding_rules: List[GcpComputeForwardingRule] = compute_forwarding_rules or []
        self.compute_ssl_policy: List[GcpComputeSslPolicy] = compute_ssl_policy or []
        self.storage_buckets: AliasesDict[GcpStorageBucket] = storage_buckets or AliasesDict()

    @functools.lru_cache(maxsize=None)
    def get_all_network_entities(self) -> Set[NetworkEntity]:
        condition: Callable = lambda resource: isinstance(resource, NetworkEntity)
        return self.get_all_mergeable_resources(condition)
