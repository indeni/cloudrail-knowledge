from typing import Dict, List

from cloudrail.knowledge.rules.base_rule import BaseRule
from cloudrail.knowledge.rules.gcp.context_aware.compute_ssl_policy_proxy_no_weak_ciphers_rule import ComputeSslPolicyProxyNoWeakCiphersRule
from cloudrail.knowledge.rules.gcp.context_aware.storage_bucket_is_not_publicly_accessible_rule import StorageBucketIsNotPubliclyAccessibleRule
from cloudrail.knowledge.rules.gcp.non_context_aware.cloud_dns_no_rsasha1_used_rules import CloudDnsNoRsasha1UsedRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_ensure_no_ip_forwarding_rule import \
    ComputeInstanceEnsureNoIpForwardingRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_subnetwork_enable_flow_logs_rule import ComputeSubNetworkEnableFlowLogsRule
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_is_not_public_rule import ContainerClusterIsNotPublictRule
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_use_rbac_users_rule import ContainerClusterUseRbacUsersRule
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_database_temp_log_files_zero_rule import PostgresDatabaseTempLogFilesZeroRule
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_log_checkpoints_rule import PostgresLogCheckpointsRule
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_log_connections_rule import PostgresLogConnectionsRule
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_log_disconnections_rule import PostgresLogDisconnectionsRule
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_log_lock_waits_on_rule import PostgresLogLockWaitsOnRule
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_log_minimum_error_rule import PostgresLogMinimumErrorRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_instance_backup_configuration_enabled_rule import SqlDatabaseBackupConfigurationEnabledRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_do_not_use_default_service_account_rule import ComputeInstanceDoNotUseDefaultServiceAccountRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_do_not_use_default_service_account_full_access_scope_rule import ComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_cross_databases_ownership_chaining_rule import SqlCrossDatabasesOwnershipChainingRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_authentication_disable_rule import SqlDatabaseAuthenticationDisableRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_instance_no_public_ip_rule import \
    SqlDatabaseNoPublicIpRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_ssl_required_rule import SqlDatabaseSslRequiredRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_log_min_duration_disable_rule import SqlLogMinimumDurationDisableRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_restrict_trusted_ip_rule import SqlDatabaseRestrictTrustedIpRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_no_serial_port_connection_rule import ComputeInstanceNoSerialPortConnectionRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_launch_with_vm_shield_rule import ComputeInstanceLaunchWithVmShieldRule
from cloudrail.knowledge.rules.gcp.context_aware.public_access_vpc_port_rule import PublicAccessVpcSshPortRule, PublicAccessVpcRdpPortRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_no_public_ip_rule import ComputeInstanceNoPublicIpRule
from cloudrail.knowledge.rules.abstract_rules_loader import AbstractRulesLoader
from cloudrail.knowledge.rules.gcp.non_context_aware.storage_bucket_logging_enabled_rule import StorageBucketLoggingEnabledRule


class GcpRulesLoader(AbstractRulesLoader):

    def load(self) -> Dict[str, BaseRule]:
        rules: List[BaseRule] = [
            SqlDatabaseSslRequiredRule(),
            SqlDatabaseRestrictTrustedIpRule(),
            SqlDatabaseNoPublicIpRule(),
            ComputeInstanceNoSerialPortConnectionRule(),
            ComputeInstanceLaunchWithVmShieldRule(),
            ComputeInstanceNoPublicIpRule(),
            SqlDatabaseBackupConfigurationEnabledRule(),
            ComputeInstanceDoNotUseDefaultServiceAccountRule(),
            SqlDatabaseAuthenticationDisableRule(),
            ComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule(),
            SqlCrossDatabasesOwnershipChainingRule(),
            ComputeInstanceEnsureNoIpForwardingRule(),
            SqlLogMinimumDurationDisableRule(),
            PostgresDatabaseTempLogFilesZeroRule(),
            PostgresLogLockWaitsOnRule(),
            PostgresLogDisconnectionsRule(),
            PostgresLogConnectionsRule(),
            ContainerClusterIsNotPublictRule(),
            PostgresLogCheckpointsRule(),
            PostgresLogMinimumErrorRule(),
            StorageBucketLoggingEnabledRule(),
            PublicAccessVpcSshPortRule(),
            CloudDnsNoRsasha1UsedRule(),
            ComputeSslPolicyProxyNoWeakCiphersRule(),
            ComputeSubNetworkEnableFlowLogsRule(),
            ContainerClusterUseRbacUsersRule(),
            PublicAccessVpcRdpPortRule(),
            StorageBucketIsNotPubliclyAccessibleRule(),
        ]
        return {rule.get_id(): rule for rule in rules}
