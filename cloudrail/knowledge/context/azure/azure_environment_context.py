from typing import List, Dict

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.azure.azure_resource_group import AzureResourceGroup
from cloudrail.knowledge.context.azure.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.context.azure.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.network.azure_nsg import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.network.azure_security_group_to_subnet_association import \
    AzureSecurityGroupToSubnetAssociation
from cloudrail.knowledge.context.azure.network.azure_subnet import AzureSubnet
from cloudrail.knowledge.context.azure.network.azure_nsg_to_nic_association import \
    AzureNetworkSecurityGroupToNicAssociation
from cloudrail.knowledge.context.azure.network.azure_nic import AzureNic
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext, CheckovResult


class AzureEnvironmentContext(BaseEnvironmentContext):

    def __init__(self,
                 checkov_results: Dict[str, List[CheckovResult]] = None,
                 resource_groups: AliasesDict[AzureResourceGroup] = None,
                 sql_servers: AliasesDict[AzureSqlServer] = None,
                 net_security_groups: AliasesDict[AzureNetworkSecurityGroup] = None,
                 subnet_network_security_group_association: List[AzureSecurityGroupToSubnetAssociation] = None,
                 subnets: AliasesDict[AzureSubnet] = None,
                 nic_network_security_group_association: List[AzureNetworkSecurityGroupToNicAssociation] = None,
                 network_interfaces: AliasesDict[AzureNic] = None,
                 app_services: AliasesDict[AzureAppService] = None,
                 app_service_configs: AliasesDict[AzureAppServiceConfig] = None,
                 function_apps: AliasesDict[AzureFunctionApp] = None):
        BaseEnvironmentContext.__init__(self)
        self.checkov_results: Dict[str, List[CheckovResult]] = checkov_results or {}
        self.resource_groups: AliasesDict[AzureResourceGroup] = resource_groups or AliasesDict()
        self.sql_servers: AliasesDict[AzureSqlServer] = sql_servers or AliasesDict()
        self.net_security_groups: AliasesDict[AzureNetworkSecurityGroup] = net_security_groups or AliasesDict()
        self.app_services: AliasesDict[AzureAppService] = app_services or AliasesDict()
        self.subnet_network_security_group_association: List[AzureSecurityGroupToSubnetAssociation] = subnet_network_security_group_association or []
        self.subnets: AliasesDict[AzureSubnet] = subnets or AliasesDict()
        self.nic_network_security_group_association: List[AzureNetworkSecurityGroupToNicAssociation] = nic_network_security_group_association or []
        self.network_interfaces: AliasesDict[AzureNic] = network_interfaces or AliasesDict()
        self.app_service_configs: AliasesDict[AzureAppServiceConfig] = app_service_configs or AliasesDict()
        self.function_apps: AliasesDict[AzureFunctionApp] = function_apps or AliasesDict()
