import json
from typing import Optional

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources_builders.terraform.app_service_builder import AppServiceBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.app_service_config_builder import AppServiceConfigBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.application_security_group_builder import ApplicationSecurityGroupBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.assigned_user_identity_builder import AssignedUserIdentityBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.batch_account_builder import BatchAccountBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.cosmos_db_account_builder import \
    CosmosDBAccountBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.data_lake_analytics_account_builder import DataLakeAnalyticsAccountBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.data_lake_store_builder import AzureDataLakeStoreBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.event_hub.event_hub_namespace_builder import EventHubNamespaceBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.event_hub.event_hub_network_rule_set_builder import EventHubNetworkRuleSetBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.function_app_builder import FunctionAppBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.function_app_config_builder import FunctionAppConfigBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.iot_hub_builder import IoTHubBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.network_interface_nat_rule_association_builder import NetworkInterfaceNatRuleAssociationBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.virtual_network_builder import VirtualNetworkBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.load_balancer_probe_builder import LoadBalancerProbeBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.load_balancer_nat_rule_builder import LoadBalancerNatRuleBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.vm_extension_builder import VmssBasicExtensionBuilder, VmssNestedExtensionBuilder, VmExtensionBuilder
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.utils.terraform_output_validator import TerraformOutputValidator
from cloudrail.knowledge.context.azure.resources_builders.terraform.keyvault_builder import KeyVaultBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.kubernetes_cluster_builder import KubernetesClusterBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.load_balancer_builder import LoadBalancerBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.logic_app_workflow_builder import LogicAppWorkflowBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.managed_disk_builder import ManagedDiskBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.monitor_activity_log_alert_builder import MonitorActivityLogAlertBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.monitor_diagnostic_setting_builder import MonitorDiagnosticSettingBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.my_sql_server_builder import MySqlServerBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.network_interface_application_security_group_association import \
    AzureNetworkInterfaceApplicationSecurityGroupAssociationBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.network_interface_builder import NetworkInterfaceBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.network_interface_security_group_association_builder import \
    AzureNetworkInterfaceSecurityGroupAssociationBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.network_security_group_builder import NetworkSecurityGroupBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.network_security_group_rule_builder import NetworkSecurityGroupRuleBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.postgresql_configuration_builder import \
    AzurePostgreSqlServerConfigurationBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.postgresql_server_builder import PostgreSqlServerBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.public_ip_builder import PublicIpBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.search_service_builder import SearchServiceBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.security_center_auto_provisioning_builder import \
    SecurityCenterAutoProvisioningBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.security_center_contact_builder import SecurityCenterContactBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.security_center_subscription_pricing_builder import \
    SecurityCenterSubscriptionPricingBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.service_bus_namespace_builder import ServiceBusNamespaceBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.sql_server_builder import MsSqlServerBuilder, StandardSqlServerBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.sql_server_extended_auditing_policy_builder import \
    SqlServerExtendedAuditingPolicyBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.sql_server_security_alert_policy_builder import \
    SqlServerSecurityAlertPolicyBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.sql_server_transparent_data_encryption_builder import \
    SqlServerTransparentEncryptionDataBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.sql_server_vulnerability_assessment_builder import \
    SqlServerVulnerabilityAssessmentBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.storage_account_builder import StorageAccountBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.storage_account_customer_managed_key_builder import \
    StorageAccountCustomerManagedKeyBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.storage_account_network_rule_builder import StorageAccountNetworkRuleBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.stream_analytics_job_builder import StreamAnalyticsJobBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.subnet_builder import SubnetBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.subnet_network_security_group_association_builder import \
    SecurityGroupToSubnetAssociationBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.subscription_builder import SubscriptionBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.virtual_machine_builder import VirtualMachineBuilder, LinuxVirtualMachineBuilder, \
    WindowsVirtualMachineBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.virtual_machine_scale_set_builder import VirtualMachineScaleSetBuilder, \
    LinuxVirtualMachineScaleSetBuilder, \
    WindowsVirtualMachineScaleSetBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.vnet_gateway_builder import VnetGatewayBuilder
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder
from cloudrail.knowledge.context.environment_context.terraform_resources_helper import get_raw_resources_by_type
from cloudrail.knowledge.context.environment_context.terraform_resources_metadata_parser import TerraformResourcesMetadataParser
from cloudrail.knowledge.context.environment_context.terraform_unknown_blocks_parser import TerraformUnknownBlocksParser
from cloudrail.knowledge.utils.checkov_utils import to_checkov_results


class AzureTerraformContextBuilder(IacContextBuilder):

    @staticmethod
    def build(iac_file: str,
              account_id: str,
              scanner_environment_context: Optional[BaseEnvironmentContext] = None,
              salt: Optional[str] = None,
              **extra_args) -> AzureEnvironmentContext:
        tenant_id = extra_args.get('tenant_id') or '00000000-0000-0000-0000-000000000000'
        iac_url_template: Optional[str] = extra_args.get('iac_url_template')
        if not iac_file:
            return AzureEnvironmentContext()
        with open(iac_file, 'r+') as file:
            data = file.read()
            TerraformOutputValidator.validate(data)
            dic = json.loads(data)
            resources_metadata = TerraformResourcesMetadataParser.parse(dic['configuration'])
            resources = get_raw_resources_by_type(dic['resource_changes'], resources_metadata)
            for resource in resources.values():
                for entity in resource:
                    entity['subscription_id'] = account_id
                    entity['tenant_id'] = tenant_id
                    entity['iac_url_template'] = iac_url_template

            virtual_machines = VirtualMachineBuilder(resources).build() + \
                               LinuxVirtualMachineBuilder(resources).build() + \
                               WindowsVirtualMachineBuilder(resources).build()
            virtual_machines_scale_sets = VirtualMachineScaleSetBuilder(resources).build() + \
                                          LinuxVirtualMachineScaleSetBuilder(resources).build() + \
                                          WindowsVirtualMachineScaleSetBuilder(resources).build()
            vmss_extentions = VmssBasicExtensionBuilder(resources).build() + VmssNestedExtensionBuilder(resources).build() + VmExtensionBuilder(resources).build()
            sql_servers = MsSqlServerBuilder(resources).build() + StandardSqlServerBuilder(resources).build()

            context: AzureEnvironmentContext = AzureEnvironmentContext()
            context.unknown_blocks = TerraformUnknownBlocksParser.parse(dic['resource_changes'])
            context.sql_servers = AliasesDict(*sql_servers)
            context.app_services = AliasesDict(*AppServiceBuilder(resources).build())
            context.app_service_configs = AliasesDict(*AppServiceConfigBuilder(resources).build())
            context.function_apps = AliasesDict(*FunctionAppBuilder(resources).build())
            context.function_app_configs = AliasesDict(*FunctionAppConfigBuilder(resources).build())
            context.net_security_groups = AliasesDict(*NetworkSecurityGroupBuilder(resources).build())
            context.subnet_network_security_group_association = SecurityGroupToSubnetAssociationBuilder(resources).build()
            context.subnets = AliasesDict(*SubnetBuilder(resources).build())
            context.network_interfaces = AliasesDict(*NetworkInterfaceBuilder(resources).build())
            context.network_interface_network_security_group_association = AzureNetworkInterfaceSecurityGroupAssociationBuilder(resources).build()
            context.vnet_gateways = AliasesDict(*VnetGatewayBuilder(resources).build())
            context.security_center_contacts = AliasesDict(*SecurityCenterContactBuilder(resources).build())
            context.security_center_auto_provisioning = AliasesDict(*SecurityCenterAutoProvisioningBuilder(resources).build())
            context.storage_accounts = AliasesDict(*StorageAccountBuilder(resources).build())
            context.storage_accounts_customer_managed_key = AliasesDict(*StorageAccountCustomerManagedKeyBuilder(resources).build())
            context.storage_account_network_rules = AliasesDict(*StorageAccountNetworkRuleBuilder(resources).build())
            context.postgresql_servers = AliasesDict(*PostgreSqlServerBuilder(resources).build())
            context.postgresql_servers_configuration = AliasesDict(*AzurePostgreSqlServerConfigurationBuilder(resources).build())
            context.security_center_subscription_pricings = SecurityCenterSubscriptionPricingBuilder(resources).build()
            context.my_sql_servers = AliasesDict(*MySqlServerBuilder(resources).build())
            context.sql_server_extended_audit_policies = AliasesDict(*SqlServerExtendedAuditingPolicyBuilder(resources).build())
            context.virtual_machines = AliasesDict(*virtual_machines)
            context.virtual_machines_scale_sets = AliasesDict(*virtual_machines_scale_sets)
            context.public_ips = AliasesDict(*PublicIpBuilder(resources).build())
            context.network_security_group_rules = NetworkSecurityGroupRuleBuilder(resources).build()
            context.app_security_groups = AliasesDict(*ApplicationSecurityGroupBuilder(resources).build())
            context.network_interface_application_security_group_association = AliasesDict(
                *AzureNetworkInterfaceApplicationSecurityGroupAssociationBuilder(resources).build())
            context.key_vaults = AliasesDict(*KeyVaultBuilder(resources).build())
            context.monitor_diagnostic_settings = AliasesDict(*MonitorDiagnosticSettingBuilder(resources).build())
            context.monitor_activity_log_alert = AliasesDict(*MonitorActivityLogAlertBuilder(resources).build())
            context.kubernetes_cluster = AliasesDict(*KubernetesClusterBuilder(resources).build())
            context.managed_disks = AliasesDict(*ManagedDiskBuilder(resources).build())
            context.cosmos_db_account = AliasesDict(*CosmosDBAccountBuilder(resources).build())
            context.data_lake_analytics_accounts = AliasesDict(*DataLakeAnalyticsAccountBuilder(resources).build())
            context.data_lake_store = AliasesDict(*AzureDataLakeStoreBuilder(resources).build())
            context.subscriptions = AliasesDict(*SubscriptionBuilder(resources).build())
            context.batch_accounts = AliasesDict(*BatchAccountBuilder(resources).build())
            context.iot_hubs = AliasesDict(*IoTHubBuilder(resources).build())
            context.logic_app_workflows = AliasesDict(*LogicAppWorkflowBuilder(resources).build())
            context.search_services = AliasesDict(*SearchServiceBuilder(resources).build())
            context.service_bus_namespaces = AliasesDict(*ServiceBusNamespaceBuilder(resources).build())
            context.stream_analytics_jobs = AliasesDict(*StreamAnalyticsJobBuilder(resources).build())
            context.vms_extentions = AliasesDict(*vmss_extentions)

            context.checkov_results = to_checkov_results(dic.get('checkov_results', {}))
            context.event_hub_namespaces = AliasesDict(*EventHubNamespaceBuilder(resources).build())
            context.event_hub_network_rule_sets = AliasesDict(*EventHubNetworkRuleSetBuilder(resources).build())
            context.assigned_user_identities = AliasesDict(*AssignedUserIdentityBuilder(resources).build())
            context.sql_server_vulnerability_assessments = AliasesDict(*SqlServerVulnerabilityAssessmentBuilder(resources).build())
            context.sql_server_security_alert_policies = AliasesDict(*SqlServerSecurityAlertPolicyBuilder(resources).build())
            context.sql_server_transparent_data_encryptions = AliasesDict(*SqlServerTransparentEncryptionDataBuilder(resources).build())
            context.virtual_networks = AliasesDict(*VirtualNetworkBuilder(resources).build())
            context.load_balancers = AliasesDict(*LoadBalancerBuilder(resources).build())
            context.load_balancer_probes = AliasesDict(*LoadBalancerProbeBuilder(resources).build())
            context.load_balancer_nat_rules = AliasesDict(*LoadBalancerNatRuleBuilder(resources).build())
            context.network_interface_nat_rule_associations = AliasesDict(*NetworkInterfaceNatRuleAssociationBuilder(resources).build())
            return context
