from typing import Optional, List
from enum import Enum

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import \
    AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_vulnerability_assessment import AzureMsSqlServerVulnerabilityAssessment


class AzureMsSqlServerSecurityAlertPolicyDisabledAlerts(Enum):
    ACCESS_ANOMALY = 'Access_Anomaly'
    SQL_INJECTION = 'Sql_Injection'
    SQL_INJECTION_VULNERABILITY = 'Sql_Injection_Vulnerability'
    DATA_EXFILTRATION = 'Data_Exfiltration'
    UNSAFE_ACTION = 'Unsafe_Action'

class AzureMsSqlServerSecurityAlertPolicyState(Enum):
    DISABLED = 'Disabled'
    ENABLED = 'Enabled'


class AzureMsSqlServerSecurityAlertPolicy(AzureResource):
    """
        Attributes:
            server_name: Specifies the name of the MS SQL Server.
            state: Specifies the state of the policy.
            disabled_alerts: Specifies an array of alerts that are disabled.
            email_account_admins: Boolean flag which specifies if the alert is sent to the account administrators or not.
            email_addresses: Specifies an array of e-mail addresses to which the alert is sent.
            retention_days: Specifies the number of days to keep in the Threat Detection audit logs.
            storage_account_access_key: Specifies the identifier key of the Threat Detection audit storage account.
            storage_endpoint: Specifies the blob storage endpoint.
    """

    def __init__(self,
                server_name: str,
                state: AzureMsSqlServerSecurityAlertPolicyState,
                disabled_alerts: Optional[List[AzureMsSqlServerSecurityAlertPolicyDisabledAlerts]],
                email_account_admins: bool,
                email_addresses: Optional[List[str]],
                retention_days: int,
                storage_account_access_key: Optional[str],
                storage_endpoint: Optional[str]):
        super().__init__(AzureResourceType.AZURERM_MSSQL_SERVER_SECURITY_ALERT_POLICY)
        self.server_name: str = server_name
        self.state: AzureMsSqlServerSecurityAlertPolicyState = state
        self.disabled_alerts: Optional[List[AzureMsSqlServerSecurityAlertPolicyDisabledAlerts]] = disabled_alerts
        self.email_account_admins: bool = email_account_admins
        self.email_addresses: Optional[List[str]] = email_addresses
        self.retention_days: int = retention_days
        self.storage_account_access_key: Optional[str] = storage_account_access_key
        self.storage_endpoint: Optional[str] = storage_endpoint
        self.vulnerability_assessment: AzureMsSqlServerVulnerabilityAssessment = None

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.server_name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self._id}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return False

    def get_type(self, is_plural: bool = False) -> str:
        return 'Azure SQL server security alert ' + ('policies' if is_plural else 'policy')

    def to_drift_detection_object(self) -> dict:
        return {'server_name': self.server_name,
                'state': self.state,
                'disabled_alerts': self.disabled_alerts,
                'email_account_admins': self.email_account_admins,
                'email_addresses': self.email_addresses,
                'retention_days': self.retention_days,
                'storage_account_access_key': self.storage_account_access_key,
                'storage_endpoint': self.storage_endpoint,
                'vulnerability_assessment': self.vulnerability_assessment and self.vulnerability_assessment.to_drift_detection_object()}
