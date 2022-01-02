import logging
import os
from typing import Optional
from cloudrail.knowledge.context.aliases_dict import AliasesDict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_global_forwarding_rule_builder import \
    ComputeGlobalForwardingRuleBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_forwarding_rule_builder import ComputeForwardingRuleBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_network_builder import ComputeNetworkBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_subnetwork_builder import ComputeSubNetworkBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_target_http_proxy_builder import \
    ComputeTargetHttpProxyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_target_ssl_proxy_builder import ComputeTargetSslProxyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_target_https_proxy_builder import \
    ComputeTargetHttpsProxyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.iam_policy_builder import StorageBucketIamPolicyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.sql_database_instance_builder import SqlDatabaseInstanceBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_instance_builder import ComputeInstanceBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_firewall_builder import ComputeFirewallBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_target_pool_builder import ComputeTargetPoolBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_ssl_policy_builder import ComputeSslPolicyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.project_builder import ProjectBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.container_cluster_builder import ContainerClusterBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.dns_managed_zone_builder import GcpDnsManagedZoneBuilder
from cloudrail.knowledge.context.environment_context.scanner_context_builder import ScannerContextBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.storage_bucket_builder import StorageBucketBuilder


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
            context.compute_networks = AliasesDict(*[network for network in ComputeNetworkBuilder(*builder_args).build() if network.get_name() == 'default'])
            return context

        context.sql_database_instances = SqlDatabaseInstanceBuilder(*builder_args).build()
        context.compute_instances = ComputeInstanceBuilder(*builder_args).build()
        context.compute_firewalls = ComputeFirewallBuilder(*builder_args).build()
        context.compute_networks = AliasesDict(*ComputeNetworkBuilder(*builder_args).build())
        context.compute_subnetworks = AliasesDict(*ComputeSubNetworkBuilder(*builder_args).build())
        context.projects = ProjectBuilder(*builder_args).build()
        context.container_cluster = ContainerClusterBuilder(*builder_args).build()
        context.compute_target_http_proxy = AliasesDict(*ComputeTargetHttpProxyBuilder(*builder_args).build())
        context.compute_target_ssl_proxy = AliasesDict(*ComputeTargetSslProxyBuilder(*builder_args).build())
        context.compute_target_https_proxy = AliasesDict(*ComputeTargetHttpsProxyBuilder(*builder_args).build())
        context.compute_global_forwarding_rule = ComputeGlobalForwardingRuleBuilder(*builder_args).build()
        context.compute_ssl_policy = AliasesDict(*ComputeSslPolicyBuilder(*builder_args).build())
        context.storage_buckets = AliasesDict(*StorageBucketBuilder(*builder_args).build())
        context.dns_managed_zones = GcpDnsManagedZoneBuilder(*builder_args).build()
        context.compute_target_pools = AliasesDict(*ComputeTargetPoolBuilder(*builder_args).build())
        context.compute_forwarding_rules = ComputeForwardingRuleBuilder(*builder_args).build()
        context.storage_bucket_iam_policies = StorageBucketIamPolicyBuilder(*builder_args).build()
        return context
