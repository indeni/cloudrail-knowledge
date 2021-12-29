import json
from typing import Optional
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_forwarding_rule_builder import ComputeForwardingRuleBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_target_ssl_proxy_builder import ComputeTargetSslProxyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_target_https_proxy_builder import \
    ComputeTargetHttpsProxyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.container_cluster_builder import ContainerClusterBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_target_http_proxy_builder import \
    ComputeTargetHttpProxyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_global_forwarding_rule_builder import \
    ComputeGlobalForwardingRuleBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.storage_bucket_builder import StorageBucketBuilder
from cloudrail.knowledge.utils.terraform_output_validator import TerraformOutputValidator
from cloudrail.knowledge.context.environment_context.terraform_resources_helper import get_raw_resources_by_type
from cloudrail.knowledge.context.environment_context.terraform_resources_metadata_parser import TerraformResourcesMetadataParser
from cloudrail.knowledge.context.gcp.resources_builders.terraform.sql_database_instance_builder import SqlDatabaseInstanceBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_network_builder import ComputeNetworkBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_subnetwork_builder import ComputeSubNetworkBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_instance_builder import ComputeInstanceBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_firewall_builder import ComputeFirewallBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_ssl_policy_builder import ComputeSslPolicyBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.dns_managed_zone_builder import GcpDnsManagedZoneBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.project_builder import ProjectBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.compute_target_pool_builder import ComputeTargetPoolBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.iam_policy_builder import StorageBucketIamPolicyBuilder
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder
from cloudrail.knowledge.utils.checkov_utils import to_checkov_results


class GcpTerraformContextBuilder(IacContextBuilder):

    @staticmethod
    def build(iac_file: str,
              account_id: str,
              scanner_environment_context: Optional[BaseEnvironmentContext] = None,
              salt: Optional[str] = None,
              **extra_args) -> GcpEnvironmentContext:
        if not iac_file:
            return GcpEnvironmentContext()
        iac_url_template: Optional[str] = extra_args.get('iac_url_template')
        with open(iac_file, 'r+') as file:
            data = file.read()
            TerraformOutputValidator.validate(data)
            dic = json.loads(data)
            resources_metadata = TerraformResourcesMetadataParser.parse(dic['configuration'])
            resources = get_raw_resources_by_type(dic['resource_changes'], resources_metadata)
            for resource in resources.values():
                for entity in resource:
                    entity['_project_id'] = account_id
                    entity['iac_url_template'] = iac_url_template

            context: GcpEnvironmentContext = GcpEnvironmentContext()
            context.checkov_results = to_checkov_results(dic.get('checkov_results', {}))

            context.sql_database_instances = SqlDatabaseInstanceBuilder(resources).build()
            context.compute_instances = ComputeInstanceBuilder(resources).build()
            context.compute_firewalls = ComputeFirewallBuilder(resources).build()
            context.compute_networks = AliasesDict(*ComputeNetworkBuilder(resources).build())
            context.compute_subnetworks = AliasesDict(*ComputeSubNetworkBuilder(resources).build())
            context.projects = ProjectBuilder(resources).build()
            context.container_cluster = ContainerClusterBuilder(resources).build()
            context.compute_target_http_proxy = AliasesDict(*ComputeTargetHttpProxyBuilder(resources).build())
            context.compute_target_ssl_proxy = AliasesDict(*ComputeTargetSslProxyBuilder(resources).build())
            context.compute_target_https_proxy = AliasesDict(*ComputeTargetHttpsProxyBuilder(resources).build())
            context.compute_global_forwarding_rule = ComputeGlobalForwardingRuleBuilder(resources).build()
            context.compute_ssl_policy = AliasesDict(*ComputeSslPolicyBuilder(resources).build())
            context.storage_buckets = AliasesDict(*StorageBucketBuilder(resources).build())
            context.dns_managed_zones = GcpDnsManagedZoneBuilder(resources).build()
            context.compute_target_pools = AliasesDict(*ComputeTargetPoolBuilder(resources).build())
            context.compute_forwarding_rules = ComputeForwardingRuleBuilder(resources).build()
            context.storage_bucket_iam_policies = StorageBucketIamPolicyBuilder.get_iam_policies(StorageBucketIamPolicyBuilder, resources)
            return context
