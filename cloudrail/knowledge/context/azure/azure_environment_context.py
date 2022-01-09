import functools

from typing import Dict, List, Set, Callable
from cloudrail.knowledge.context.aliases_dict import AliasesDict

from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server_configuration import \
    AzurePostgreSqlServerConfiguration
from cloudrail.knowledge.context.azure.resources.iot.azure_iot_hub import AzureIoTHub
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_vulnerability_assessment import AzureMsSqlServerVulnerabilityAssessment
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_security_alert_policy import AzureMsSqlServerSecurityAlertPolicy
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_transparent_data_encryption import AzureMsSqlServerTransparentDataEncryption
from cloudrail.knowledge.context.azure.resources.event_hub.azure_event_hub_namespace import AzureEventHubNamespace
from cloudrail.knowledge.context.azure.resources.event_hub.event_hub_network_rule_set import EventHubNetworkRuleSet
from cloudrail.knowledge.context.azure.resources.i_managed_identity_resource import IManagedIdentityResource
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer import AzureLoadBalancer
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_user_assigned_identity import AzureAssignedUserIdentity
from cloudrail.knowledge.context.azure.resources.monitor.azure_activity_log_alert import AzureMonitorActivityLogAlert
from cloudrail.knowledge.context.azure.resources.aks.azure_kubernetes_cluster import AzureKubernetesCluster
from cloudrail.knowledge.context.azure.resources.azure_resource_group import AzureResourceGroup
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_nat_rule_association import AzureNetworkInterfaceNatRuleAssociation
from cloudrail.knowledge.context.azure.resources.network.azure_virtual_network import AzureVirtualNetwork
from cloudrail.knowledge.context.azure.resources.search.azure_search_service import AzureSearchService
from cloudrail.knowledge.context.azure.resources.service_bus.azure_service_bus_namespace import AzureServiceBusNamespace
from cloudrail.knowledge.context.azure.resources.storage.azure_data_lake_analytics_account import AzureDataLakeAnalyticsAccount
from cloudrail.knowledge.context.azure.resources.databases.azure_cosmos_db_account import AzureCosmosDBAccount
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import AzureSqlServerExtendedAuditingPolicy
from cloudrail.knowledge.context.azure.resources.databases.azure_mysql_server import AzureMySqlServer
from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server import AzurePostgreSqlServer
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.context.azure.resources.disk.azure_managed_disk import AzureManagedDisk
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.keyvault.azure_key_vault import AzureKeyVault
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting
from cloudrail.knowledge.context.azure.resources.network.azure_application_security_group import AzureApplicationSecurityGroup
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import AzureNetworkInterface
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_application_security_group_association import \
    AzureNetworkInterfaceApplicationSecurityGroupAssociation
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_security_group_association import AzureNetworkInterfaceSecurityGroupAssociation
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group_rule import AzureNetworkSecurityRule
from cloudrail.knowledge.context.azure.resources.network.azure_public_ip import AzurePublicIp
from cloudrail.knowledge.context.azure.resources.network.azure_security_group_to_subnet_association import AzureSecurityGroupToSubnetAssociation
from cloudrail.knowledge.context.azure.resources.network.azure_subnet import AzureSubnet
from cloudrail.knowledge.context.azure.resources.network.azure_vnet_gateway import AzureVirtualNetworkGateway
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_auto_provisioning import AzureSecurityCenterAutoProvisioning
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_contact import AzureSecurityCenterContact
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_subscription_pricing import AzureSecurityCenterSubscriptionPricing
from cloudrail.knowledge.context.azure.resources.storage.azure_data_lake_store import AzureDataLakeStore
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_customer_managed_key import AzureStorageAccountCustomerManagedKey
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules
from cloudrail.knowledge.context.azure.resources.stream_analytics.azure_stream_analytics_job import AzureStreamAnalyticsJob
from cloudrail.knowledge.context.azure.resources.subscription.azure_subscription import AzureSubscription
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer_probe import AzureLoadBalancerProbe
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer_nat_rule import AzureLoadBalancerNatRule
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine_extension import AzureVirtualMachineExtension
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.azure.resources.webapp.web_app_stack import WebAppStack
from cloudrail.knowledge.context.azure.resources.logic_app.azure_logic_app_workflow import AzureLogicAppWorkflow
from cloudrail.knowledge.context.azure.resources.batch_management.azure_batch_account import AzureBatchAccount
from cloudrail.knowledge.context.base_environment_context import (BaseEnvironmentContext, CheckovResult)


class AzureEnvironmentContext(BaseEnvironmentContext):

    def __init__(self,
                 checkov_results: Dict[str, List[CheckovResult]] = None,
                 resource_groups: AliasesDict[AzureResourceGroup] = None,
                 sql_servers: AliasesDict[AzureSqlServer] = None,
                 net_security_groups: AliasesDict[AzureNetworkSecurityGroup] = None,
                 subnet_network_security_group_association: List[AzureSecurityGroupToSubnetAssociation] = None,
                 subnets: AliasesDict[AzureSubnet] = None,
                 network_interface_network_security_group_association: List[AzureNetworkInterfaceSecurityGroupAssociation] = None,
                 network_interfaces: AliasesDict[AzureNetworkInterface] = None,
                 app_services: AliasesDict[AzureAppService] = None,
                 app_service_configs: AliasesDict[AzureAppServiceConfig] = None,
                 web_app_stacks: AliasesDict[WebAppStack] = None,
                 function_apps: AliasesDict[AzureFunctionApp] = None,
                 function_app_configs: AliasesDict[AzureAppServiceConfig] = None,
                 vnet_gateways: AliasesDict[AzureVirtualNetworkGateway] = None,
                 security_center_contacts: AliasesDict[AzureSecurityCenterContact] = None,
                 security_center_subscription_pricings: List[AzureSecurityCenterSubscriptionPricing] = None,
                 my_sql_servers: AliasesDict[AzureMySqlServer] = None,
                 sql_server_extended_audit_policies: AliasesDict[AzureSqlServerExtendedAuditingPolicy] = None,
                 postgresql_servers: AliasesDict[AzurePostgreSqlServer] = None,
                 postgresql_servers_configuration: AliasesDict[AzurePostgreSqlServerConfiguration] = None,
                 storage_accounts: AliasesDict[AzureStorageAccount] = None,
                 storage_accounts_customer_managed_key: AliasesDict[AzureStorageAccountCustomerManagedKey] = None,
                 storage_account_network_rules: AliasesDict[AzureStorageAccountNetworkRules] = None,
                 security_center_auto_provisioning: AliasesDict[AzureSecurityCenterAutoProvisioning] = None,
                 key_vaults: AliasesDict[AzureKeyVault] = None,
                 kubernetes_cluster: AliasesDict[AzureKubernetesCluster] = None,
                 monitor_diagnostic_settings: AliasesDict[AzureMonitorDiagnosticSetting] = None,
                 monitor_activity_log_alert: AliasesDict[AzureMonitorActivityLogAlert] = None,
                 managed_disks: AliasesDict[AzureManagedDisk] = None,
                 virtual_machines: AliasesDict[AzureVirtualMachine] = None,
                 public_ips: AliasesDict[AzurePublicIp] = None,
                 network_security_group_rules: List[AzureNetworkSecurityRule] = None,
                 app_security_groups: AliasesDict[AzureApplicationSecurityGroup] = None,
                 nic_application_security_group_association: AliasesDict[AzureNetworkInterfaceApplicationSecurityGroupAssociation] = None,
                 virtual_machines_scale_sets: AliasesDict[AzureVirtualMachineScaleSet] = None,
                 cosmos_db_account: AliasesDict[AzureCosmosDBAccount] = None,
                 data_lake_analytics_accounts: AliasesDict[AzureDataLakeAnalyticsAccount] = None,
                 data_lake_store: AliasesDict[AzureDataLakeStore] = None,
                 subscriptions: AliasesDict[AzureSubscription] = None,
                 batch_accounts: AliasesDict[AzureBatchAccount] = None,
                 iot_hubs: AliasesDict[AzureIoTHub] = None,
                 logic_app_workflows: AliasesDict[AzureLogicAppWorkflow] = None,
                 search_services: AliasesDict[AzureSearchService] = None,
                 service_bus_namespaces: AliasesDict[AzureServiceBusNamespace] = None,
                 stream_analytics_jobs: AliasesDict[AzureStreamAnalyticsJob] = None,
                 vms_extentions: AliasesDict[AzureVirtualMachineExtension] = None,
                 event_hub_namespaces: AliasesDict[AzureEventHubNamespace] = None,
                 event_hub_network_rule_sets: AliasesDict[EventHubNetworkRuleSet] = None,
                 assigned_user_identities: AliasesDict[AzureAssignedUserIdentity] = None,
                 sql_server_vulnerability_assessments: AliasesDict[AzureMsSqlServerVulnerabilityAssessment] = None,
                 sql_server_security_alert_policies: AliasesDict[AzureMsSqlServerSecurityAlertPolicy] = None,
                 sql_server_transparent_data_encryptions: AliasesDict[AzureMsSqlServerTransparentDataEncryption] = None,
                 virtual_networks: AliasesDict[AzureVirtualNetwork] = None,
                 load_balancers: AliasesDict[AzureLoadBalancer] = None,
                 load_balancer_probes: AliasesDict[AzureLoadBalancerProbe] = None,
                 load_balancer_nat_rules: AliasesDict[AzureLoadBalancerNatRule] = None,
                 network_interface_nat_rule_associations: AliasesDict[AzureNetworkInterfaceNatRuleAssociation] = None,
                 ):
        BaseEnvironmentContext.__init__(self)
        self.checkov_results: Dict[str, List[CheckovResult]] = checkov_results or {}
        self.resource_groups: AliasesDict[AzureResourceGroup] = resource_groups or AliasesDict()
        self.sql_servers: AliasesDict[AzureSqlServer] = sql_servers or AliasesDict()
        self.net_security_groups: AliasesDict[AzureNetworkSecurityGroup] = net_security_groups or AliasesDict()
        self.app_services: AliasesDict[AzureAppService] = app_services or AliasesDict()
        self.subnet_network_security_group_association: List[AzureSecurityGroupToSubnetAssociation] = subnet_network_security_group_association or []
        self.subnets: AliasesDict[AzureSubnet] = subnets or AliasesDict()
        self.network_interface_network_security_group_association: List[AzureNetworkInterfaceSecurityGroupAssociation] = \
            network_interface_network_security_group_association or []
        self.network_interfaces: AliasesDict[AzureNetworkInterface] = network_interfaces or AliasesDict()
        self.app_service_configs: AliasesDict[AzureAppServiceConfig] = app_service_configs or AliasesDict()
        self.web_app_stacks: AliasesDict[WebAppStack] = web_app_stacks or AliasesDict()
        self.function_apps: AliasesDict[AzureFunctionApp] = function_apps or AliasesDict()
        self.function_app_configs: AliasesDict[AzureAppServiceConfig] = function_app_configs or AliasesDict()
        self.security_center_auto_provisioning: AliasesDict[AzureSecurityCenterAutoProvisioning] = security_center_auto_provisioning or AliasesDict()
        self.security_center_contacts: AliasesDict[AzureSecurityCenterContact] = security_center_contacts or AliasesDict()
        self.vnet_gateways: AliasesDict[AzureVirtualNetworkGateway] = vnet_gateways or AliasesDict()
        self.security_center_subscription_pricings: List[AzureSecurityCenterSubscriptionPricing] = security_center_subscription_pricings or []
        self.postgresql_servers: AliasesDict[AzurePostgreSqlServer] = postgresql_servers or AliasesDict()
        self.my_sql_servers: AliasesDict[AzureMySqlServer] = my_sql_servers or AliasesDict()
        self.sql_server_extended_audit_policies: AliasesDict[AzureSqlServerExtendedAuditingPolicy] = sql_server_extended_audit_policies or AliasesDict()
        self.storage_accounts: AliasesDict[AzureStorageAccount] = storage_accounts or AliasesDict()
        self.storage_accounts_customer_managed_key: AliasesDict[AzureStorageAccountCustomerManagedKey] = storage_accounts_customer_managed_key or AliasesDict()
        self.storage_account_network_rules: AliasesDict[AzureStorageAccountNetworkRules] = storage_account_network_rules or AliasesDict()
        self.key_vaults: AliasesDict[AzureKeyVault] = key_vaults or AliasesDict()
        self.monitor_diagnostic_settings: AliasesDict[AzureMonitorDiagnosticSetting] = monitor_diagnostic_settings or AliasesDict()
        self.monitor_activity_log_alert: AliasesDict[AzureMonitorActivityLogAlert] = monitor_activity_log_alert or AliasesDict()
        self.kubernetes_cluster: AliasesDict[AzureKubernetesCluster] = kubernetes_cluster or AliasesDict()
        self.managed_disks: AliasesDict[AzureManagedDisk] = managed_disks or AliasesDict()
        self.virtual_machines: AliasesDict[AzureVirtualMachine] = virtual_machines or AliasesDict()
        self.public_ips: AliasesDict[AzurePublicIp] = public_ips or AliasesDict()
        self.network_security_group_rules: List[AzureNetworkSecurityRule] = network_security_group_rules or []
        self.app_security_groups: AliasesDict[AzureApplicationSecurityGroup] = app_security_groups or AliasesDict()
        self.network_interface_application_security_group_association: AliasesDict[AzureNetworkInterfaceApplicationSecurityGroupAssociation] = \
            nic_application_security_group_association or AliasesDict()
        self.virtual_machines_scale_sets: AliasesDict[AzureVirtualMachineScaleSet] = virtual_machines_scale_sets or AliasesDict()
        self.cosmos_db_account: AliasesDict[AzureCosmosDBAccount] = cosmos_db_account or AliasesDict()
        self.data_lake_analytics_accounts: AliasesDict[AzureDataLakeAnalyticsAccount] = data_lake_analytics_accounts or AliasesDict()
        self.data_lake_store: AliasesDict[AzureDataLakeStore] = data_lake_store or AliasesDict()
        self.subscriptions: AliasesDict[AzureSubscription] = subscriptions or AliasesDict()
        self.batch_accounts: AliasesDict[AzureBatchAccount] = batch_accounts or AliasesDict()
        self.postgresql_servers_configuration: AliasesDict[AzurePostgreSqlServerConfiguration] = postgresql_servers_configuration or AliasesDict()
        self.iot_hubs: AliasesDict[AzureIoTHub] = iot_hubs or AliasesDict()
        self.logic_app_workflows: AliasesDict[AzureLogicAppWorkflow] = logic_app_workflows or AliasesDict()
        self.search_services: AliasesDict[AzureSearchService] = search_services or AliasesDict()
        self.service_bus_namespaces: AliasesDict[AzureServiceBusNamespace] = service_bus_namespaces or AliasesDict()
        self.stream_analytics_jobs: AliasesDict[AzureStreamAnalyticsJob] = stream_analytics_jobs or AliasesDict()
        self.vms_extentions: AliasesDict[AzureVirtualMachineExtension] = vms_extentions or AliasesDict()
        self.event_hub_namespaces: AliasesDict[AzureEventHubNamespace] = event_hub_namespaces or AliasesDict()
        self.event_hub_network_rule_sets: AliasesDict[EventHubNetworkRuleSet] = event_hub_network_rule_sets or AliasesDict()
        self.assigned_user_identities: AliasesDict[AzureAssignedUserIdentity] = assigned_user_identities or AliasesDict()
        self.sql_server_vulnerability_assessments: AliasesDict[AzureMsSqlServerVulnerabilityAssessment] = sql_server_vulnerability_assessments or AliasesDict()
        self.sql_server_security_alert_policies: AliasesDict[AzureMsSqlServerSecurityAlertPolicy] = sql_server_security_alert_policies or AliasesDict()
        self.sql_server_transparent_data_encryptions: AliasesDict[AzureMsSqlServerTransparentDataEncryption] = sql_server_transparent_data_encryptions or AliasesDict()
        self.virtual_networks: AliasesDict[AzureVirtualNetwork] = virtual_networks or AliasesDict()
        self.load_balancers: AliasesDict[AzureLoadBalancer] = load_balancers or AliasesDict()
        self.load_balancer_probes: AliasesDict[AzureLoadBalancerProbe] = load_balancer_probes or AliasesDict()
        self.load_balancer_nat_rules: AliasesDict[AzureLoadBalancerNatRule] = load_balancer_nat_rules or AliasesDict()
        self.network_interface_nat_rule_associations: AliasesDict[AzureNetworkInterfaceNatRuleAssociation] = \
            network_interface_nat_rule_associations or AliasesDict()

    @functools.lru_cache(maxsize=None)
    def get_all_monitored_resources(self) -> Set[IMonitorSettings]:
        condition: Callable = lambda azure_resource: isinstance(azure_resource, IMonitorSettings)
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_assigned_user_identity_resources(self) -> Set[IMonitorSettings]:
        condition: Callable = lambda azure_resource: isinstance(azure_resource, IManagedIdentityResource)
        return self.get_all_mergeable_resources(condition)
