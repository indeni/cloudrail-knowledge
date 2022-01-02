from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_security_alert_policy import AzureMsSqlServerSecurityAlertPolicy, \
    AzureMsSqlServerSecurityAlertPolicyState, AzureMsSqlServerSecurityAlertPolicyDisabledAlerts
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation
from cloudrail.knowledge.utils.utils import is_iterable_with_values

class SqlServerSecurityAlertPolicyBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'sql-servers-security-alert-policies.json'

    def do_build(self, attributes: dict) -> AzureMsSqlServerSecurityAlertPolicy:
        properties= attributes['properties']
        ## Disabled Alerts
        disabled_alerts = []
        for alert in properties['disabledAlerts']:
            disabled_alerts.append(enum_implementation(AzureMsSqlServerSecurityAlertPolicyDisabledAlerts, alert))
        disabled_alerts = disabled_alerts if is_iterable_with_values(disabled_alerts) else []

        email_addresses = properties['emailAddresses']
        email_addresses = email_addresses if is_iterable_with_values(email_addresses) else []

        storage_account_access_key = properties['storageAccountAccessKey'] if properties['storageAccountAccessKey'] else None
        storage_endpoint = properties['storageEndpoint'] if properties['storageEndpoint'] else None
        return AzureMsSqlServerSecurityAlertPolicy(server_name=attributes['id'].split('/')[-3],
                                                   state=enum_implementation(AzureMsSqlServerSecurityAlertPolicyState, properties['state']),
                                                   disabled_alerts=disabled_alerts,
                                                   email_account_admins=properties['emailAccountAdmins'],
                                                   email_addresses=email_addresses,
                                                   retention_days=properties['retentionDays'],
                                                   storage_account_access_key=storage_account_access_key,
                                                   storage_endpoint=storage_endpoint)
