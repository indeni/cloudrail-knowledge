from enum import Enum


class AzureResourceType(Enum):
    NONE = 'none'
    AZURERM_RESOURCE_GROUP = 'azurerm_resource_group'
    AZURERM_SQL_SERVER = 'azurerm_sql_server'
    AZURERM_POSTGRESQL_SERVER = 'azurerm_postgresql_server'
    AZURERM_MYSQL_SERVER = 'azurerm_mysql_server'
    AZURERM_MSSQL_SERVER = 'azurerm_mssql_server'
    AZURERM_SQL_FIREWALL_RULE = 'azurerm_sql_firewall_rule'
    AZURERM_APP_SERVICE = 'azurerm_app_service'
    AZURERM_NETWORK_SECURITY_GROUP = 'azurerm_network_security_group'
    AZURERM_SUBNET_NETWORK_SECURITY_GROUP_ASSOCIATION = 'azurerm_subnet_network_security_group_association'
    AZURERM_NETWORK_INTERFACE_SECURITY_GROUP_ASSOCIATION = 'azurerm_network_interface_security_group_association'
    AZURERM_SUBNET = 'azurerm_subnet'
    AZURERM_NETWORK_INTERFACE = 'azurerm_network_interface'
    AZURERM_FUNCTION_APP = 'azurerm_function_app'
    AZURERM_SECURITY_CENTER_AUTO_PROVISIONING = 'azurerm_security_center_auto_provisioning'
    AZURERM_SECURITY_CENTER_CONTACT = 'azurerm_security_center_contact'
    AZURERM_VIRTUAL_NETWORK_GATEWAY = 'azurerm_virtual_network_gateway'
    AZURERM_SECURITY_CENTER_SUBSCRIPTION_PRICING = 'azurerm_security_center_subscription_pricing'
    AZURERM_MSSQL_SERVER_EXTENDED_AUDITING_POLICY = 'azurerm_mssql_server_extended_auditing_policy'
    AZURERM_STORAGE_ACCOUNT = 'azurerm_storage_account'
