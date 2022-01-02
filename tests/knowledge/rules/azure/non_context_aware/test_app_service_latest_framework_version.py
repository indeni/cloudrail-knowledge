from typing import Dict
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.rules.azure_rules_loader import AzureRulesLoader
from cloudrail.knowledge.rules.base_rule import RuleResultType, BaseRule


class TestServiceAppUseLatestFrameworkVersionRule(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.rules_map: Dict[str, BaseRule] = AzureRulesLoader().load()

    @parameterized.expand(
        [
            ['non_car_service_app_using_latest_python_version', 'Python|3.9', False],
            ['non_car_service_app_using_latest_python_version', 'Python|3.10', False],
            ['non_car_service_app_using_latest_python_version', 'Python|3.8', True],
            ['non_car_service_app_using_latest_python_version', '', False],
            ['non_car_service_app_using_latest_java_version', 'JAVA|11', False],
            ['non_car_service_app_using_latest_java_version', 'JAVA|11.10', False],
            ['non_car_service_app_using_latest_java_version', 'JAVA|10', True],
            ['non_car_service_app_using_latest_java_version', '', False],
            ['non_car_web_app_using_latest_php_version', 'PHP|7.4', False],
            ['non_car_web_app_using_latest_php_version', 'PHP|8.0', False],
            ['non_car_web_app_using_latest_php_version', 'PHP|7.3', True],
            ['non_car_web_app_using_latest_php_version', '', False]
        ]
    )
    def test_non_car_function_app_using_latest_python_version_fail(self, rule_id: str, linux_fx_version: str, should_alert: bool):
        # Arrange
        service_app: AzureAppService = create_empty_entity(AzureAppService)
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.linux_fx_version = linux_fx_version
        service_app.app_service_config = app_service_config
        service_app.name = 'my-service-app'
        service_app.with_aliases(service_app.name)
        context = AzureEnvironmentContext(app_services=AliasesDict(*[service_app]))
        # Act
        result = self.rules_map.get(rule_id).run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))