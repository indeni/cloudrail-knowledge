import functools
from typing import Dict, List, Set, Callable

from cloudrail.knowledge.context.azure.resources.monitor.azure_activity_log_alert import AzureMonitorActivityLogAlert

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.resources.aks.azure_kubernetes_cluster import AzureKubernetesCluster
from cloudrail.knowledge.context.azure.resources.azure_resource_group import AzureResourceGroup
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
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules
from cloudrail.knowledge.context.azure.resources.subscription.azure_subscription import AzureSubscription
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet
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
                 storage_accounts: AliasesDict[AzureStorageAccount] = None,
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
                 logic_app_workflows: AliasesDict[AzureLogicAppWorkflow] = None,
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
        self.logic_app_workflows: AliasesDict[AzureLogicAppWorkflow] = logic_app_workflows or AliasesDict()

    @functools.lru_cache(maxsize=None)
    def get_all_monitored_resources(self) -> Set[IMonitorSettings]:
        condition: Callable = lambda aws_resource: isinstance(aws_resource, IMonitorSettings)
        return self.get_all_mergeable_resources(condition)
