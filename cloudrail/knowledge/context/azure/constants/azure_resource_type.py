from enum import Enum


class AzureResourceType(Enum):

    AZURERM_RESOURCE_GROUP = 'azurerm_resource_group'
    AZURERM_SQL_SERVER = 'azurerm_sql_server'
    AZURERM_MSSQL_SERVER = 'azurerm_mssql_server'
    AZURERM_SQL_FIREWALL_RULE = 'azurerm_sql_firewall_rule'
    AZURERM_APP_SERVICE = 'azurerm_app_service'
    AZURERM_NETWORK_SECURITY_GROUP = 'azurerm_network_security_group'
    AZURERM_SUBNET_NETWORK_SECURITY_GROUP_ASSOCIATION = 'azurerm_subnet_network_security_group_association'
    AZURERM_NETWORK_INTERFACE_SECURITY_GROUP_ASSOCIATION = 'azurerm_network_interface_security_group_association'
    AZURERM_SUBNET = 'azurerm_subnet'
    AZURERM_NETWORK_INTERFACE = 'azurerm_network_interface'
