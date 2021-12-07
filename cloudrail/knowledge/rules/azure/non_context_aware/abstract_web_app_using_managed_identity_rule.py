from abc import abstractmethod
from typing import List, Dict, Union

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AbstractWebAppUsingManagedIdentityRule(AzureBaseRule):

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        pass

    @abstractmethod
    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[Union[AzureAppService,
                                                                                                       AzureFunctionApp]]:
        pass

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for web_app in self.get_web_app_resources(env_context):
            if not web_app.identity:
                issues.append(
                    Issue(
                        f'The {web_app.get_type()} `{web_app.get_friendly_name()}` '
                        f'does not use managed identity.', web_app, web_app))
        return issues


class FunctionAppUseManagedIdentityRule(AbstractWebAppUsingManagedIdentityRule):
    def get_id(self) -> str:
        return 'non_car_function_app_using_managed_identity'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.function_apps)

    @abstractmethod
    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[AzureFunctionApp]:
        return environment_context.function_apps


class AppServiceUseManagedIdentityRule(AbstractWebAppUsingManagedIdentityRule):

    def get_id(self) -> str:
        return 'non_car_web_app_using_managed_identity'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.app_services)

    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[AzureAppService]:
        return environment_context.app_services
