import logging
import os
from typing import Optional

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources_builders.scanner.assigned_user_identity_builder import AssignedUserIdentityBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.data_lake_store_builder import DataLakeStoreBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.event_hub.event_hub_namespace_builder import EventHubNamespaceBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.event_hub.event_hub_network_rule_set_builder import EventHubNetworkRuleSetBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.keyvault_builder import KeyVaultBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.kubernetes_cluster_builder import KubernetesClusterBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.managed_disk_builder import ManagedDiskBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.monitor_diagnostic_setting_builder import MonitorDiagnosticSettingBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.app_service_builder import AppServiceBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.app_service_config_builder import AppServiceConfigBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.application_security_group_builder import ApplicationSecurityGroupBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.function_app_builder import FunctionAppBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.network_interface_nat_rule_association_builder import NetworkInterfaceNatRuleAssociationBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.network_interface_security_group_association_builder import \
    AzureNetworkInterfaceSecurityGroupAssociationBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.postgresql_server_builder import PostgreSqlServerBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.postgresql_server_configuration_builder import \
    AzurePostgreSqlServerConfigurationBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.public_ip_builder import PublicIpBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.my_sql_server_builder import MySqlServerBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.search_service_builder import SearchServiceBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.security_center_auto_provisioning_builder import \
    SecurityCenterAutoProvisioningBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.security_center_contact_builder import SecurityCenterContactBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.security_center_subscription_pricing_builder import \
    SecurityCenterSubscriptionPricingBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.sql_server_builder import SqlServerBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.subscription_builder import SubscriptionBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.storage_account_builder import StorageAccountBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.storage_account_customer_managed_key_builder import StorageAccountCustomerManagedKeyBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.storage_account_network_rule_builder import StorageAccountNetworkRuleBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.network_security_group_builder import NetworkSecurityGroupBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.network_interface_builder import NetworkInterfaceBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.sql_server_extended_auditing_policy_builder import \
    SqlServerExtendedAuditingPolicyBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.subnet_builder import SubnetsBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.subnet_network_security_group_association_builder import \
    SecurityGroupToSubnetAssociationBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.virtual_machine_builder import VirtualMachineBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.virtual_machine_scale_set_builder import VirtualMachineScaleSetBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.virtual_network_builder import VirtualNetworkBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.load_balancer_builder import LoadBalancerBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.load_balancer_probe_builder import LoadBalancerProbeBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.load_balancer_nat_rule_builder import LoadBalancerNatRuleBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.vm_extension_builder import VmssExtensionBuilder, VmExtensionBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.vnet_gateway_builder import VnetGatewayBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.iot_hub_builder import IoTHubBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.cosmos_db_account_builder import CosmosDBAccountBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.web_app_stacks_builder import WebAppStacksBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.batch_account_builder import BatchAccountBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.logic_app_workflow_builder import LogicAppWorkflowBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.monitor_activity_log_alert_builder import MonitorActivityLogAlertBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.data_lake_analytics_account_builder import DataLakeAnalyticsAccountBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.service_bus_namespace_builder import ServiceBusNamespaceBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.stream_analytics_job_builder import StreamAnalyticsJobBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.sql_server_vulnerability_assessment_builder import SqlServerVulnerabilityAssessmentBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.sql_server_security_alert_policy_builder import SqlServerSecurityAlertPolicyBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.sql_server_transparent_data_encryption_builder import \
    SqlServerTransparentEncryptionDataBuilder
from cloudrail.knowledge.context.environment_context.scanner_context_builder import ScannerContextBuilder


class AzureScannerContextBuilder(ScannerContextBuilder):

    @staticmethod
    def build(account_data_dir: Optional[str], account_id: Optional[str], salt: Optional[str] = None, **extra_args) -> AzureEnvironmentContext:
        if not account_data_dir:
            return AzureEnvironmentContext()
        if not os.path.exists(account_data_dir):
            logging.warning('cloud mapper working dir does not exists: {}'.format(account_data_dir))
            return AzureEnvironmentContext()
        builder_args = (account_data_dir, account_id, extra_args.get('tenant_id'))
        all_vms_extenstions = VmssExtensionBuilder(*builder_args).build() + VmExtensionBuilder(*builder_args).build()

        context: AzureEnvironmentContext = AzureEnvironmentContext()
        context.sql_servers = AliasesDict(*SqlServerBuilder(*builder_args).build())
        context.net_security_groups = AliasesDict(*NetworkSecurityGroupBuilder(*builder_args).build())
        context.network_interfaces = AliasesDict(*NetworkInterfaceBuilder(*builder_args).build())
        context.subnets = AliasesDict(*SubnetsBuilder(*builder_args).build())
        context.app_services = AliasesDict(*AppServiceBuilder(*builder_args).build())
        context.app_service_configs = AliasesDict(*AppServiceConfigBuilder(*builder_args).build())
        context.web_app_stacks = AliasesDict(*WebAppStacksBuilder(*builder_args).build())
        context.function_apps = AliasesDict(*FunctionAppBuilder(*builder_args).build())
        context.function_app_configs = AliasesDict(*AppServiceConfigBuilder(*builder_args).build())
        context.vnet_gateways = AliasesDict(*VnetGatewayBuilder(*builder_args).build())
        context.security_center_contacts = AliasesDict(*SecurityCenterContactBuilder(*builder_args).build())
        context.security_center_auto_provisioning = AliasesDict(*SecurityCenterAutoProvisioningBuilder(*builder_args).build())
        context.storage_accounts = AliasesDict(*StorageAccountBuilder(*builder_args).build())
        context.storage_accounts_customer_managed_key = AliasesDict(*StorageAccountCustomerManagedKeyBuilder(*builder_args).build())
        context.storage_account_network_rules = AliasesDict(*StorageAccountNetworkRuleBuilder(*builder_args).build())
        context.postgresql_servers = AliasesDict(*PostgreSqlServerBuilder(*builder_args).build())
        context.postgresql_servers_configuration = AliasesDict(*AzurePostgreSqlServerConfigurationBuilder(*builder_args).build())
        context.security_center_subscription_pricings = SecurityCenterSubscriptionPricingBuilder(*builder_args).build()
        context.my_sql_servers = AliasesDict(*MySqlServerBuilder(*builder_args).build())
        context.sql_server_extended_audit_policies = AliasesDict(*SqlServerExtendedAuditingPolicyBuilder(*builder_args).build())
        context.virtual_machines = AliasesDict(*VirtualMachineBuilder(*builder_args).build())
        context.public_ips = AliasesDict(*PublicIpBuilder(*builder_args).build())
        context.app_security_groups = AliasesDict(*ApplicationSecurityGroupBuilder(*builder_args).build())
        context.key_vaults = AliasesDict(*KeyVaultBuilder(*builder_args).build())
        context.monitor_diagnostic_settings = AliasesDict(*MonitorDiagnosticSettingBuilder(*builder_args).build())
        context.monitor_activity_log_alert = AliasesDict(*MonitorActivityLogAlertBuilder(*builder_args).build())
        context.kubernetes_cluster = AliasesDict(*KubernetesClusterBuilder(*builder_args).build())
        context.managed_disks = AliasesDict(*ManagedDiskBuilder(*builder_args).build())
        context.virtual_machines_scale_sets = AliasesDict(*VirtualMachineScaleSetBuilder(*builder_args).build())
        context.subnet_network_security_group_association = SecurityGroupToSubnetAssociationBuilder(*builder_args).build()
        context.network_interface_network_security_group_association = AzureNetworkInterfaceSecurityGroupAssociationBuilder(*builder_args).build()
        context.cosmos_db_account = AliasesDict(*CosmosDBAccountBuilder(*builder_args).build())
        context.data_lake_analytics_accounts = AliasesDict(*DataLakeAnalyticsAccountBuilder(*builder_args).build())
        context.data_lake_store = AliasesDict(*DataLakeStoreBuilder(*builder_args).build())
        context.subscriptions = AliasesDict(*SubscriptionBuilder(*builder_args).build())
        context.batch_accounts = AliasesDict(*BatchAccountBuilder(*builder_args).build())
        context.iot_hubs = AliasesDict(*IoTHubBuilder(*builder_args).build())
        context.logic_app_workflows = AliasesDict(*LogicAppWorkflowBuilder(*builder_args).build())
        context.search_services = AliasesDict(*SearchServiceBuilder(*builder_args).build())
        context.service_bus_namespaces = AliasesDict(*ServiceBusNamespaceBuilder(*builder_args).build())
        context.stream_analytics_jobs = AliasesDict(*StreamAnalyticsJobBuilder(*builder_args).build())
        context.vms_extentions = AliasesDict(*all_vms_extenstions)
        context.event_hub_namespaces = AliasesDict(*EventHubNamespaceBuilder(*builder_args).build())
        context.event_hub_network_rule_sets = AliasesDict(*EventHubNetworkRuleSetBuilder(*builder_args).build())
        context.assigned_user_identities = AliasesDict(*AssignedUserIdentityBuilder(*builder_args).build())
        context.sql_server_vulnerability_assessments = AliasesDict(*SqlServerVulnerabilityAssessmentBuilder(*builder_args).build())
        context.sql_server_security_alert_policies = AliasesDict(*SqlServerSecurityAlertPolicyBuilder(*builder_args).build())
        context.sql_server_transparent_data_encryptions = AliasesDict(*SqlServerTransparentEncryptionDataBuilder(*builder_args).build())
        context.virtual_networks = AliasesDict(*VirtualNetworkBuilder(*builder_args).build())
        context.load_balancers = AliasesDict(*LoadBalancerBuilder(*builder_args).build())
        context.load_balancer_probes = AliasesDict(*LoadBalancerProbeBuilder(*builder_args).build())
        context.load_balancer_nat_rules = AliasesDict(*LoadBalancerNatRuleBuilder(*builder_args).build())
        context.network_interface_nat_rule_associations = AliasesDict(*NetworkInterfaceNatRuleAssociationBuilder(*builder_args).build())
        return context
