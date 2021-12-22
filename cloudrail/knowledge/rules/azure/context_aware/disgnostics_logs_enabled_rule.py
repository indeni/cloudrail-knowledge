from abc import abstractmethod
from typing import Iterable, List, Dict, Union

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AbstractDiagnosticLogsRule(AzureBaseRule):

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for resource in self.get_resources(env_context):
            evidence_msg = f'{resource.get_type()} `{resource.get_friendly_name()}`'
            if not resource.get_monitor_settings():
                issues.append(Issue(f'The {evidence_msg} does not have diagnostic settings', resource, resource))
            else:
                for monitor_settings in resource.get_monitor_settings():

                    monitor_msg = f'The Monitor Diagnostic Setting {monitor_settings.name}, associated to {evidence_msg},'
                    if not monitor_settings.logs_settings:
                        issues.append(Issue(f'{monitor_msg} does not have log block configuration', resource, monitor_settings))
                    elif not monitor_settings.logs_settings.enabled:
                        issues.append(Issue(f'{monitor_msg} does not have log enabled', resource, monitor_settings))
                    elif not monitor_settings.logs_settings.retention_policy:
                        issues.append(Issue(f'{monitor_msg} does not have a log retention policy', resource, monitor_settings))
                    elif not monitor_settings.logs_settings.retention_policy.enabled:
                        issues.append(Issue(f'{monitor_msg} have a disabled log retention policy', resource, monitor_settings))
                    elif 0 < monitor_settings.logs_settings.retention_policy.days < 365:
                        issues.append(Issue(f'{monitor_msg} does not have a log retention policy days equal to 0 or greater than or equal to 365',
                                            resource, monitor_settings))

        return issues

    @abstractmethod
    def get_id(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_resources(env_context: AzureEnvironmentContext) -> Iterable[Union[Mergeable, IMonitorSettings]]:
        pass

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(self.get_resources(environment_context))


class KeyVaultDiagnosticLogsEnabledRule(AbstractDiagnosticLogsRule):

    def get_id(self) -> str:
        return 'car_key_vault_diagnostic_logs_enabled'

    @staticmethod
    def get_resources(env_context: AzureEnvironmentContext):
        return env_context.key_vaults


class DataLakeAnalyticsDiagnosticLogsEnabledRule(AbstractDiagnosticLogsRule):

    def get_id(self) -> str:
        return 'car_data_lake_analytics_account_diagnostic_logs_enabled'

    @staticmethod
    def get_resources(env_context: AzureEnvironmentContext) -> Iterable[Union[Mergeable, IMonitorSettings]]:
        return env_context.data_lake_analytics_accounts


class BatchAccountDiagnosticLogsEnabledRule(AbstractDiagnosticLogsRule):

    def get_id(self) -> str:
        return 'car_batch_account_diagnostic_logs_enabled'

    @staticmethod
    def get_resources(env_context: AzureEnvironmentContext) -> Iterable[Union[Mergeable, IMonitorSettings]]:
        return env_context.batch_accounts

class IotHubDiagnosticLogsEnabledRule(AbstractDiagnosticLogsRule):

    def get_id(self) -> str:
        return 'car_iot_hub_diagnostic_logs_enabled'

    @staticmethod
    def get_resources(env_context: AzureEnvironmentContext):
        return env_context.iot_hubs

class DataLakeStoreDiagnosticLogsEnabledRule(AbstractDiagnosticLogsRule):

    def get_id(self) -> str:
        return 'car_data_lake_store_diagnostic_logs_enabled'

    def get_resources(self, env_context: AzureEnvironmentContext) -> Iterable[Union[Mergeable, IMonitorSettings]]:
        return env_context.data_lake_store.values()

class LogicAppWorkflowDiagnosticLogsEnabledRule(AbstractDiagnosticLogsRule):

    def get_id(self) -> str:
        return 'car_logic_app_workflow_diagnostic_logs_enabled'

    def get_resources(self, env_context: AzureEnvironmentContext) -> Iterable[Union[Mergeable, IMonitorSettings]]:
        return env_context.logic_app_workflows

class SearchServiceDiagnosticLogsEnabledRule(AbstractDiagnosticLogsRule):

    def get_id(self) -> str:
        return 'car_search_service_diagnostic_logs_enabled'

    def get_resources(self, env_context: AzureEnvironmentContext) -> Iterable[Union[Mergeable, IMonitorSettings]]:
        return env_context.search_services

class ServiceBusNamespaceDiagnosticLogsEnabledRule(AbstractDiagnosticLogsRule):

    def get_id(self) -> str:
        return 'car_service_bus_namespace_diagnostic_logs_enabled'

    def get_resources(self, env_context: AzureEnvironmentContext) -> Iterable[Union[Mergeable, IMonitorSettings]]:
        return env_context.service_bus_namespaces

class StreamAnalyitcsJobDiagnosticLogsEnabledRule(AbstractDiagnosticLogsRule):

    def get_id(self) -> str:
        return 'car_stream_analytics_job_diagnostic_logs_enabled'

    def get_resources(self, env_context: AzureEnvironmentContext) -> Iterable[Union[Mergeable, IMonitorSettings]]:
        return env_context.stream_analytics_jobs
