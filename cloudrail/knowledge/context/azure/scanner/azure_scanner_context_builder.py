import logging
import os
from typing import Optional

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources_builders.scanner.keyvault_builder import KeyVaultBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.kubernetes_cluster_builder import KubernetesClusterBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.managed_disk_builder import ManagedDiskBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.monitor_diagnostic_setting_builder import MonitorDiagnosticSettingBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.app_service_builder import AppServiceBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.app_service_config_builder import AppServiceConfigBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.application_security_group_builder import ApplicationSecurityGroupBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.function_app_builder import FunctionAppBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.network_interface_security_group_association_builder import \
    AzureNetworkInterfaceSecurityGroupAssociationBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.postgresql_server_builder import PostgreSqlServerBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.public_ip_builder import PublicIpBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.my_sql_server_builder import MySqlServerBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.security_center_auto_provisioning_builder import \
    SecurityCenterAutoProvisioningBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.security_center_contact_builder import SecurityCenterContactBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.security_center_subscription_pricing_builder import \
    SecurityCenterSubscriptionPricingBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.sql_server_builder import SqlServerBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.storage_account_builder import StorageAccountBuilder
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
from cloudrail.knowledge.context.azure.resources_builders.scanner.vnet_gateway_builder import VnetGatewayBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.cosmos_db_account_builder import CosmosDBAccountBuilder
from cloudrail.knowledge.context.azure.resources_builders.scanner.web_app_stacks_builder import WebAppStacksBuilder
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
        context.storage_account_network_rules = AliasesDict(*StorageAccountNetworkRuleBuilder(*builder_args).build())
        context.postgresql_servers = AliasesDict(*PostgreSqlServerBuilder(*builder_args).build())
        context.security_center_subscription_pricings = SecurityCenterSubscriptionPricingBuilder(*builder_args).build()
        context.my_sql_servers = AliasesDict(*MySqlServerBuilder(*builder_args).build())
        context.sql_server_extended_audit_policies = AliasesDict(*SqlServerExtendedAuditingPolicyBuilder(*builder_args).build())
        context.virtual_machines = AliasesDict(*VirtualMachineBuilder(*builder_args).build())
        context.public_ips = AliasesDict(*PublicIpBuilder(*builder_args).build())
        context.app_security_groups = AliasesDict(*ApplicationSecurityGroupBuilder(*builder_args).build())
        context.key_vaults = AliasesDict(*KeyVaultBuilder(*builder_args).build())
        context.monitor_diagnostic_settings = AliasesDict(*MonitorDiagnosticSettingBuilder(*builder_args).build())
        context.kubernetes_cluster = AliasesDict(*KubernetesClusterBuilder(*builder_args).build())
        context.managed_disks = AliasesDict(*ManagedDiskBuilder(*builder_args).build())
        context.virtual_machines_scale_sets = AliasesDict(*VirtualMachineScaleSetBuilder(*builder_args).build())
        context.subnet_network_security_group_association = SecurityGroupToSubnetAssociationBuilder(*builder_args).build()
        context.network_interface_network_security_group_association = AzureNetworkInterfaceSecurityGroupAssociationBuilder(*builder_args).build()
        context.cosmos_db_account = AliasesDict(*CosmosDBAccountBuilder(*builder_args).build())
        return context
