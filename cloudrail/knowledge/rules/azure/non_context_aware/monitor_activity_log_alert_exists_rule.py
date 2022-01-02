from abc import abstractmethod
from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.monitor.azure_activity_log_alert import AzureMonitorActivityLogAlert, MonitorActivityLogAlertCriteriaCategory
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class BaseMonitorActivityLogAlertExistsRule(AzureBaseRule):

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for subscription in env_context.subscriptions:
            monitors = self._get_all_relevant_monitors(subscription.monitor_activity_alert_log_list)
            # Checks if all operations name are exists
            operations_name = [monitor.criteria.operation_name for monitor in monitors]
            if any(operation_name not in operations_name for operation_name in self._get_operations_name()):
                issues.append(
                    Issue(
                        f"The {subscription.get_type()} `{subscription.subscription_id}` does not have Activity Log Alerts for Create/Update/Delete {self._get_resource_name()} events",
                        subscription,
                        subscription))
            else:
                for monitor in monitors:
                    # Checks if monitor is enabled
                    if not monitor.enabled:
                        issues.append(Issue(
                            f"The {monitor.get_type()} `{monitor.get_friendly_name()}` on '{subscription.subscription_id}' is not enabled",
                            subscription,
                            monitor))
                    # Checks if category set properly
                    elif monitor.criteria.category.value != self._get_category():
                        issues.append(Issue(
                            f"The {subscription.get_type()} `{subscription.subscription_id}` does not have Activity Log Alerts for Create/Update/Delete {self._get_resource_name()} events",
                            subscription,
                            subscription))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.subscriptions)

    @staticmethod
    def filter_non_iac_managed_issues() -> bool:
        return False

    def _get_all_relevant_monitors(self, monitors: List[AzureMonitorActivityLogAlert]) -> List[AzureMonitorActivityLogAlert]:
        return [monitor for monitor in monitors if monitor.criteria.operation_name in self._get_operations_name()]

    @abstractmethod
    def _get_operations_name(self) -> List[str]:
        pass

    @abstractmethod
    def _get_resource_name(self) -> str:
        pass

    @abstractmethod
    def _get_category(self) -> str:
        pass


class NetworkSecurityGroupRulesMonitorActivityLogAlertExistsRule(BaseMonitorActivityLogAlertExistsRule):
    def get_id(self) -> str:
        return 'non_car_activity_log_alert_create_update_delete_network_security_group_rules'

    def _get_operations_name(self) -> List[str]:
        return ["Microsoft.Network/networkSecurityGroups/securityRules/write",
                "Microsoft.Network/networkSecurityGroups/securityRules/delete",
                "Microsoft.ClassicNetwork/networkSecurityGroups/securityRules/write",
                "Microsoft.ClassicNetwork/networkSecurityGroups/securityRules/delete"]

    def _get_resource_name(self) -> str:
        return "Network Security Group Rules"

    def _get_category(self) -> str:
        return MonitorActivityLogAlertCriteriaCategory.ADMINISTRATIVE.value


class NetworkSecurityGroupMonitorActivityLogAlertExistsRule(BaseMonitorActivityLogAlertExistsRule):
    def get_id(self) -> str:
        return 'non_car_activity_log_alert_create_update_delete_network_security_groups'

    def _get_operations_name(self) -> List[str]:
        return ["Microsoft.Network/networkSecurityGroups/write",
                "Microsoft.Network/networkSecurityGroups/delete",
                "Microsoft.ClassicNetwork/networkSecurityGroups/write",
                "Microsoft.ClassicNetwork/networkSecurityGroups/delete"]

    def _get_resource_name(self) -> str:
        return "Network Security Group"

    def _get_category(self) -> str:
        return MonitorActivityLogAlertCriteriaCategory.ADMINISTRATIVE.value


class PolicyAssignmentMonitorActivityLogAlertExistsRule(BaseMonitorActivityLogAlertExistsRule):
    def get_id(self) -> str:
        return 'non_car_activity_log_alert_create_update_delete_policy_assignment'

    def _get_operations_name(self) -> List[str]:
        return ["Microsoft.Authorization/policyAssignments/write",
                "Microsoft.Authorization/policyAssignments/delete"]

    def _get_resource_name(self) -> str:
        return "Policy Assignment"

    def _get_category(self) -> str:
        return MonitorActivityLogAlertCriteriaCategory.ADMINISTRATIVE.value


class SecurityPolicyMonitorActivityLogAlertExistsRule(BaseMonitorActivityLogAlertExistsRule):
    def get_id(self) -> str:
        return 'non_car_activity_log_alert_update_security_policy'

    def _get_operations_name(self) -> List[str]:
        return ["Microsoft.Security/policies/write"]

    def _get_resource_name(self) -> str:
        return "Security Policy"

    def _get_category(self) -> str:
        return MonitorActivityLogAlertCriteriaCategory.SECURITY.value


class SecuritySolutionsMonitorActivityLogAlertExistsRule(BaseMonitorActivityLogAlertExistsRule):
    def get_id(self) -> str:
        return 'non_car_activity_log_alert_create_update_delete_security_solutions'

    def _get_operations_name(self) -> List[str]:
        return ["Microsoft.Security/securitySolutions/write",
                "Microsoft.Security/securitySolutions/delete"]

    def _get_resource_name(self) -> str:
        return "Security Solutions"

    def _get_category(self) -> str:
        return MonitorActivityLogAlertCriteriaCategory.SECURITY.value
