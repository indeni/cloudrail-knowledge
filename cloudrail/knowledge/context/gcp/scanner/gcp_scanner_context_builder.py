import logging
import os
from typing import Optional

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_global_forwarding_rule_builder import \
    ComputeGlobalForwardingRuleBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_network_builder import ComputeNetworkBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_target_http_proxy_builder import \
    ComputeTargetHttpProxyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.sql_database_instance_builder import SqlDatabaseInstanceBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_instance_builder import ComputeInstanceBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_firewall_builder import ComputeFirewallBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.project_builder import ProjectBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.container_cluster_builder import ContainerClusterBuilder
from cloudrail.knowledge.context.environment_context.scanner_context_builder import ScannerContextBuilder


class GcpScannerContextBuilder(ScannerContextBuilder):

    @staticmethod
    def build(account_data_dir: str, account_id: Optional[str], salt: Optional[str] = None, **extra_args) -> GcpEnvironmentContext:
        context: GcpEnvironmentContext = GcpEnvironmentContext()
        builder_args = (account_data_dir, account_id, salt)
        if not account_data_dir:
            return context
        if not os.path.exists(account_data_dir):
            logging.warning('scanner working dir does not exists: {}'.format(account_data_dir))
            return context
        elif extra_args.get('default_resources_only'):
            context.projects = ProjectBuilder(*builder_args).build()
            return context

        context.sql_database_instances = SqlDatabaseInstanceBuilder(*builder_args).build()
        context.compute_instances = ComputeInstanceBuilder(*builder_args).build()
        context.compute_firewalls = ComputeFirewallBuilder(*builder_args).build()
        context.compute_networks = ComputeNetworkBuilder(*builder_args).build()
        context.projects = ProjectBuilder(*builder_args).build()
        context.container_cluster = ContainerClusterBuilder(*builder_args).build()
        context.compute_target_http_proxy = ComputeTargetHttpProxyBuilder(*builder_args).build()
        context.compute_global_forwarding_rule = ComputeGlobalForwardingRuleBuilder(*builder_args).build()
        return context
