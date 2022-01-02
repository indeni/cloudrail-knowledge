from abc import abstractmethod
from typing import List, Dict, Union

from cloudrail.knowledge.context.aliases_dict import AliasesDict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class WebAppUseLatestHttpVersionRule(AzureBaseRule):

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        pass

    @abstractmethod
    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[Union[AzureAppService, AzureFunctionApp]]:
        pass

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for web_app in self.get_web_app_resources(env_context):
            if web_app.app_service_config is not None and \
                    not web_app.app_service_config.http2_enabled:
                issues.append(
                    Issue(
                        f'The {web_app.get_type()} `{web_app.get_friendly_name()}` does not use the latest HTTP version.',
                        web_app,
                        web_app))
        return issues


class FunctionAppUseLatestHttpVersionRule(WebAppUseLatestHttpVersionRule):

    def get_id(self) -> str:
        return 'non_car_http_latest_in_function_app'

    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[AzureFunctionApp]:
        return environment_context.function_apps

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.function_apps)


class AppServiceUseLatestHttpVersionRule(WebAppUseLatestHttpVersionRule):

    def get_id(self) -> str:
        return 'non_car_web_app_using_latest_http_version'

    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[AzureAppService]:
        return environment_context.app_services

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.app_services)
