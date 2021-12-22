from typing import Dict, List

from cloudrail.knowledge.rules.abstract_rules_loader import AbstractRulesLoader
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import KeyVaultDiagnosticLogsEnabledRule, \
    BatchAccountDiagnosticLogsEnabledRule, DataLakeAnalyticsDiagnosticLogsEnabledRule, DataLakeStoreDiagnosticLogsEnabledRule, \
    LogicAppWorkflowDiagnosticLogsEnabledRule, IotHubDiagnosticLogsEnabledRule, SearchServiceDiagnosticLogsEnabledRule, \
    ServiceBusNamespaceDiagnosticLogsEnabledRule, StreamAnalyitcsJobDiagnosticLogsEnabledRule
from cloudrail.knowledge.rules.azure.context_aware.not_publicly_accessible_rule import VirtualMachineNotPubliclyAccessibleRdpRule, \
    VirtualMachineNotPubliclyAccessibleSshRule
from cloudrail.knowledge.rules.azure.non_context_aware.abstract_web_app_using_managed_identity_rule import \
    FunctionAppUseManagedIdentityRule, AppServiceUseManagedIdentityRule
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_accessible_only_via_https_rule import AppServiceAccessibleOnlyViaHttpsRule
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_authentication_enable_rule import AppServiceAuthenticationEnableRule
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_ftps_required_rule import AppServiceFtpsRequiredRule
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_non_car_client_certificates_required_in_web_app_rule \
    import AppServiceClientCertificatesRequiredRule
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_non_car_diagnostic_logs_enabled_in_app_services_rule import \
    AppServiceDiagnosticLogsRule
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_use_latest_tls_version_rule import AppServiceUseLatestTlsVersionRule
from cloudrail.knowledge.rules.azure.non_context_aware.auto_provisioning_log_analytics_agent_disabled_rule import \
    AutoProvisioningLogAnalyticsAgentDisabledRule
from cloudrail.knowledge.rules.azure.non_context_aware.defender_enabled_rules import ContainerRegistriesDefenderEnabledRule, \
    SqlServersDefenderEnabledRule, StorageDefenderEnabledRule, ServersDefenderEnabledRule, KubernetesDefenderEnabledRule, \
    SqlServersOnVirtualMachinesDefenderEnabledRule, AppServicesDefenderEnabledRule, KeyVaultsDefenderEnabledRule
from cloudrail.knowledge.rules.azure.non_context_aware.email_notification_high_severity_alerts_enabled_rule import \
    EmailNotificationHighSeverityAlertsEnabledRule
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_managed_disks_encrypted_rule import EnsureManagedDisksEncryptedRule
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_sql_server_audit_enabled_rule import EnsureSqlServerAuditEnabledRule
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_storage_account_default_network_deny_rule import \
    EnsureStorageAccountDefaultNetworkDenyRule
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_vms_and_vmss_use_managed_disks_rule import EnsureVmAndVmssUseManagedDisksRule
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_accessible_only_via_https_rule import FunctionAppAccessibleOnlyViaHttpsRule
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_authentication_enable_rule import FunctionAppAuthenticationEnableRule
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_client_certificate_mode_rule import FunctionAppClientCertificateModeRule
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_enforces_ftps_only_rule import FunctionAppEnforcesFtpsOnlyRule
from cloudrail.knowledge.rules.azure.non_context_aware.monitor_activity_log_alert_exists_rule import NetworkSecurityGroupRulesMonitorActivityLogAlertExistsRule, \
    NetworkSecurityGroupMonitorActivityLogAlertExistsRule, PolicyAssignmentMonitorActivityLogAlertExistsRule, SecurityPolicyMonitorActivityLogAlertExistsRule, \
    SecuritySolutionsMonitorActivityLogAlertExistsRule
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_use_latest_tls_version_rule import FunctionAppUseLatestTlsVersionRule
from cloudrail.knowledge.rules.azure.non_context_aware.key_vault_purge_protection_enabled_rule import KeyVaultPurgeProtectionEnabledRule
from cloudrail.knowledge.rules.azure.non_context_aware.kubernetes_cluster_rbac_enabled_rule import KubernetesClusterRbacEnabledRule
from cloudrail.knowledge.rules.azure.non_context_aware.my_sql_server_enforcing_ssl_rule import MySqlServerEnforcingSslRule
from cloudrail.knowledge.rules.azure.non_context_aware.postgresql_server_enforce_ssl_rule import PostgreSqlServerEnforceSslRule
from cloudrail.knowledge.rules.azure.non_context_aware.public_access_sql_database_rule import PublicAccessSqlDatabaseRule
from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_allow_network_access_trusted_azure_services_rule import \
    StorageAccountAllowNetworkAccessTrustedAzureResourcesRule
from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_public_access_rule import StorageAccountPublicAccessRule
from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_secure_transfer import StorageAccountSecureTransferRule
from cloudrail.knowledge.rules.azure.non_context_aware.unused_network_security_group_rule import UnusedNetworkSecurityGroupRule
from cloudrail.knowledge.rules.azure.non_context_aware.vpn_gateway_disallow_basic_sku_rule import VpnGatewayDisallowBasicSkuRule
from cloudrail.knowledge.rules.azure.non_context_aware.web_app_use_http_version_rule import FunctionAppUseLatestHttpVersionRule, \
    AppServiceUseLatestHttpVersionRule
from cloudrail.knowledge.rules.azure.non_context_aware.web_app_using_latest_version_rule import \
    FunctionAppUsingLatestJavaVersionRule, FunctionAppUsingLatestPythonVersionRule, AppServiceUsingLatestPythonVersionRule, \
    AppServiceUsingLatestJavaVersionRule, AppServiceUsingLatestPhpVersionRule
from cloudrail.knowledge.rules.base_rule import BaseRule


class AzureRulesLoader(AbstractRulesLoader):

    def load(self) -> Dict[str, BaseRule]:
        rules: List[BaseRule] = [
            PublicAccessSqlDatabaseRule(),
            AppServiceFtpsRequiredRule(),
            UnusedNetworkSecurityGroupRule(),
            FunctionAppAuthenticationEnableRule(),
            FunctionAppClientCertificateModeRule(),
            VpnGatewayDisallowBasicSkuRule(),
            FunctionAppUseLatestHttpVersionRule(),
            EmailNotificationHighSeverityAlertsEnabledRule(),
            AutoProvisioningLogAnalyticsAgentDisabledRule(),
            AppServicesDefenderEnabledRule(),
            FunctionAppUseLatestTlsVersionRule(),
            KeyVaultDiagnosticLogsEnabledRule(),
            ContainerRegistriesDefenderEnabledRule(),
            SqlServersDefenderEnabledRule(),
            SqlServersOnVirtualMachinesDefenderEnabledRule(),
            KubernetesDefenderEnabledRule(),
            StorageDefenderEnabledRule(),
            ServersDefenderEnabledRule(),
            KeyVaultsDefenderEnabledRule(),
            MySqlServerEnforcingSslRule(),
            AppServiceAuthenticationEnableRule(),
            EnsureStorageAccountDefaultNetworkDenyRule(),
            EnsureSqlServerAuditEnabledRule(),
            AppServiceUseLatestTlsVersionRule(),
            AppServiceAccessibleOnlyViaHttpsRule(),
            FunctionAppAccessibleOnlyViaHttpsRule(),
            PostgreSqlServerEnforceSslRule(),
            VirtualMachineNotPubliclyAccessibleRdpRule(),
            VirtualMachineNotPubliclyAccessibleSshRule(),
            KeyVaultPurgeProtectionEnabledRule(),
            StorageAccountAllowNetworkAccessTrustedAzureResourcesRule(),
            StorageAccountSecureTransferRule(),
            StorageAccountPublicAccessRule(),
            EnsureManagedDisksEncryptedRule(),
            EnsureVmAndVmssUseManagedDisksRule(),
            AppServiceDiagnosticLogsRule(),
            KubernetesClusterRbacEnabledRule(),
            FunctionAppEnforcesFtpsOnlyRule(),
            AppServiceClientCertificatesRequiredRule(),
            FunctionAppUsingLatestJavaVersionRule(),
            FunctionAppUseManagedIdentityRule(),
            AppServiceUseManagedIdentityRule(),
            FunctionAppUsingLatestPythonVersionRule(),
            AppServiceUsingLatestPythonVersionRule(),
            AppServiceUsingLatestJavaVersionRule(),
            AppServiceUsingLatestPhpVersionRule(),
            AppServiceUseLatestHttpVersionRule(),
            DataLakeAnalyticsDiagnosticLogsEnabledRule(),
            BatchAccountDiagnosticLogsEnabledRule(),
            NetworkSecurityGroupRulesMonitorActivityLogAlertExistsRule(),
            DataLakeStoreDiagnosticLogsEnabledRule(),
            IotHubDiagnosticLogsEnabledRule(),
            DataLakeStoreDiagnosticLogsEnabledRule(),
            LogicAppWorkflowDiagnosticLogsEnabledRule(),
            NetworkSecurityGroupMonitorActivityLogAlertExistsRule(),
            PolicyAssignmentMonitorActivityLogAlertExistsRule(),
            SecurityPolicyMonitorActivityLogAlertExistsRule(),
            SecuritySolutionsMonitorActivityLogAlertExistsRule(),
            SearchServiceDiagnosticLogsEnabledRule(),
            ServiceBusNamespaceDiagnosticLogsEnabledRule(),
            StreamAnalyitcsJobDiagnosticLogsEnabledRule(),
        ]
        return {rule.get_id(): rule for rule in rules}
