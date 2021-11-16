from typing import Dict, List

from cloudrail.knowledge.rules.base_rule import BaseRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_ensure_no_ip_forwarding_rule import \
    ComputeInstanceEnsureNoIpForwardingRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_instance_backup_configuration_enabled_rule import SqlDatabaseBackupConfigurationEnabledRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_do_not_use_default_service_account_rule import ComputeInstanceDoNotUseDefaultServiceAccountRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_do_not_use_default_service_account_full_access_scope_rule import ComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_cross_databases_ownership_chaining_rule import SqlCrossDatabasesOwnershipChainingRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_authentication_disable_rule import SqlDatabaseAuthenticationDisableRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_instance_no_public_ip_rule import \
    SqlDatabaseNoPublicIpRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_ssl_required_rule import SqlDatabaseSslRequiredRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_restrict_trusted_ip_rule import SqlDatabaseRestrictTrustedIpRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_no_serial_port_connection_rule import ComputeInstanceNoSerialPortConnectionRule
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_launch_with_vm_shield_rule import ComputeInstanceLaunchWithVmShieldRule
from cloudrail.knowledge.rules.abstract_rules_loader import AbstractRulesLoader


class GcpRulesLoader(AbstractRulesLoader):

    def load(self) -> Dict[str, BaseRule]:
        rules: List[BaseRule] = [
            SqlDatabaseSslRequiredRule(),
            SqlDatabaseRestrictTrustedIpRule(),
            SqlDatabaseNoPublicIpRule(),
            ComputeInstanceNoSerialPortConnectionRule(),
            ComputeInstanceLaunchWithVmShieldRule(),
            SqlDatabaseBackupConfigurationEnabledRule(),
            ComputeInstanceDoNotUseDefaultServiceAccountRule(),
            SqlDatabaseAuthenticationDisableRule(),
            ComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule(),
            SqlCrossDatabasesOwnershipChainingRule(),
            ComputeInstanceEnsureNoIpForwardingRule(),
        ]
        return {rule.get_id(): rule for rule in rules}
