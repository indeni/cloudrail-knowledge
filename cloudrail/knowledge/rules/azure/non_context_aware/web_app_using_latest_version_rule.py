from abc import abstractmethod
from typing import List, Dict, Union, Optional, Tuple
from pkg_resources import parse_version
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.azure.resources.webapp.web_app_stack import WebAppStack
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AbstractWebAppUsingLatestVersionRule(AzureBaseRule):

    def __init__(self, code_lang: str, latest_version: str) -> None:
        super().__init__()
        self.code_lang: str = code_lang
        self.latest_version: str = latest_version    # todo - fetch latest

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
        latest_web_app_stack: WebAppStack = self._get_web_app_stack_latest_major_version(env_context)
        self.latest_version = latest_web_app_stack.get_latest_version() if latest_web_app_stack else self.latest_version
        for web_app in self.get_web_app_resources(env_context):
            code_lang, version = self._get_version(web_app.app_service_config)
            if code_lang and version and code_lang.upper() == self.code_lang.upper() and \
                    parse_version(version) < parse_version(self.latest_version):
                issues.append(
                    Issue(
                        f'The {web_app.get_type()} `{web_app.get_friendly_name()}` '
                        f'does not use the latest Azure supported {self.code_lang} version ({self.latest_version}).',
                        web_app,
                        web_app))
        return issues

    @staticmethod
    def _get_version(config: AzureAppServiceConfig) -> Tuple[str, str]:
        code_lang = None
        version = None
        if config.linux_fx_version:
            code_lang, version = tuple(config.linux_fx_version.split('|'))
            if 'java' in version:
                version = version.split('java')[1]
                code_lang = 'JAVA'
            elif 'jre' in version:
                version = version.split('jre')[1]
                code_lang = 'JAVA'
        elif config.java_version:
            code_lang = 'JAVA'
            if config.java_version.startswith('1.'):
                version = config.java_version.replace('1.', '')
            else:
                version = config.java_version
        return code_lang, version

    def _get_web_app_stack_latest_major_version(self, env_context: AzureEnvironmentContext, preferred_os: str = 'linux') -> Optional[WebAppStack]:
        web_app_stack: Optional[WebAppStack] = None
        stacks: List[WebAppStack] = [stack for stack in env_context.web_app_stacks
                                     if stack.preferred_os == preferred_os and self.code_lang.lower() in stack.get_name().lower()]
        if stacks:
            web_app_stack = stacks[0]
            for index in range(1, len(stacks)):
                if web_app_stack.major_version < stacks[index].major_version:
                    web_app_stack = stacks[index]
        return web_app_stack


class FunctionAppUsingLatestJavaVersionRule(AbstractWebAppUsingLatestVersionRule):

    def __init__(self) -> None:
        super().__init__('JAVA', '11')

    def get_id(self) -> str:
        return 'non_car_function_app_using_latest_java_version'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.function_apps)

    @abstractmethod
    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[AzureFunctionApp]:
        return environment_context.function_apps


class FunctionAppUsingLatestPythonVersionRule(AbstractWebAppUsingLatestVersionRule):

    def __init__(self) -> None:
        super().__init__('PYTHON', '3.9')

    def get_id(self) -> str:
        return 'non_car_function_app_using_latest_python_version'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.function_apps)

    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[AzureFunctionApp]:
        return environment_context.function_apps


class AppServiceUsingLatestPythonVersionRule(AbstractWebAppUsingLatestVersionRule):

    def __init__(self) -> None:
        super().__init__('PYTHON', '3.9')

    def get_id(self) -> str:
        return 'non_car_service_app_using_latest_python_version'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.app_services)

    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[AzureAppService]:
        return environment_context.app_services


class AppServiceUsingLatestJavaVersionRule(AbstractWebAppUsingLatestVersionRule):

    def __init__(self) -> None:
        super().__init__('JAVA', '11')

    def get_id(self) -> str:
        return 'non_car_service_app_using_latest_java_version'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.app_services)

    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[AzureAppService]:
        return environment_context.app_services


class AppServiceUsingLatestPhpVersionRule(AbstractWebAppUsingLatestVersionRule):

    def __init__(self) -> None:
        super().__init__('PHP', '7.4')

    def get_id(self) -> str:
        return 'non_car_web_app_using_latest_php_version'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.app_services)

    def get_web_app_resources(self, environment_context: AzureEnvironmentContext) -> AliasesDict[AzureAppService]:
        return environment_context.app_services
