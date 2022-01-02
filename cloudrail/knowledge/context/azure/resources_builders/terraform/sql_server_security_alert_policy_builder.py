from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_security_alert_policy import AzureMsSqlServerSecurityAlertPolicy, \
    AzureMsSqlServerSecurityAlertPolicyState, AzureMsSqlServerSecurityAlertPolicyDisabledAlerts
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class SqlServerSecurityAlertPolicyBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureMsSqlServerSecurityAlertPolicy:
        ## Disabled Alerts
        disabled_alerts = []
        for alert in self._get_known_value(attributes, 'disabled_alerts', []):
            disabled_alerts.append(enum_implementation(AzureMsSqlServerSecurityAlertPolicyDisabledAlerts, alert))
        return AzureMsSqlServerSecurityAlertPolicy(server_name=attributes['server_name'],
                                                   state=enum_implementation(AzureMsSqlServerSecurityAlertPolicyState, attributes['state']),
                                                   disabled_alerts=disabled_alerts,
                                                   email_account_admins=self._get_known_value(attributes, 'email_account_admins', False),
                                                   email_addresses=self._get_known_value(attributes, 'email_addresses', []),
                                                   retention_days=self._get_known_value(attributes, 'retention_days', 0),
                                                   storage_account_access_key=self._get_known_value(attributes, 'storage_account_access_key'),
                                                   storage_endpoint=self._get_known_value(attributes, 'storage_endpoint'))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_MSSQL_SERVER_SECURITY_ALERT_POLICY
