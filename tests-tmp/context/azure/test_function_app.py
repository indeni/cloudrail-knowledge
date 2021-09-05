from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.azure.webapp.constants import FieldMode
from test.knowledge.context.azure_context_test import AzureContextTest
from test.knowledge.context.test_context_annotation import context


class TestFunctionApp(AzureContextTest):

    def get_component(self):
        return "function_app"

    @context(module_path="auth_settings")
    def test_auth_settings(self, ctx: AzureEnvironmentContext):
        func_app: AzureFunctionApp = ctx.function_apps.get('my-func-app')
        self.assertIsNotNone(func_app)
        self.assertIsNotNone(func_app.app_service_config.auth_settings)
        self.assertTrue(func_app.app_service_config.auth_settings.enabled)
        self.assertEqual(func_app.client_cert_mode, FieldMode.REQUIRED)

    @context(module_path="http2/http2_enabled")
    def test_functionapp_http2_enabled(self, ctx: AzureEnvironmentContext):
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2152-functionapp')
        self.assertIsNotNone(func_app)
        self.assertTrue(func_app.app_service_config.http2_enabled)

    @context(module_path="http2/http2_disabled")
    def test_functionapp_http2_not_enabled(self, ctx: AzureEnvironmentContext):
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2152-functionapp')
        self.assertIsNotNone(func_app)
        self.assertFalse(func_app.app_service_config.http2_enabled)

    @context(module_path="tls/tls_1_1")
    def test_tls_1_1(self, ctx: AzureEnvironmentContext):
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2152ftls-functionapp')
        self.assertIsNotNone(func_app)
        self.assertEqual(func_app.app_service_config.minimum_tls_version, '1.1')

    @context(module_path="tls/tls_1_2")
    def test_tls_1_2(self, ctx: AzureEnvironmentContext):
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2152ftls-functionapp')
        self.assertIsNotNone(func_app)
        self.assertEqual(func_app.app_service_config.minimum_tls_version, '1.2')

    # ------------------- java latest version tests -------------------

    @context(module_path="language_version/functionapp_lin_java_is_latest")
    def test_functionapp_lin_java_is_latest(self, ctx: AzureEnvironmentContext):
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2152flj-functionapp')
        self.assertIsNotNone(func_app)
        self.assertEqual(func_app.app_service_config.linux_fx_version, 'JAVA|11')
        self.assertEqual(func_app.app_service_config.java_version, None)

    @context(module_path="language_version/functionapp_lin_java_isnot_latest")
    def test_functionapp_lin_java_isnot_latest(self, ctx: AzureEnvironmentContext):
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2152flj-functionapp')
        self.assertIsNotNone(func_app)
        self.assertEqual(func_app.app_service_config.linux_fx_version, 'JAVA|8')
        self.assertEqual(func_app.app_service_config.java_version, None)

    @context(module_path="language_version/functionapp_win_java_is_latest")
    def test_functionapp_win_java_is_latest(self, ctx: AzureEnvironmentContext):
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2152fwj-functionapp')
        self.assertIsNotNone(func_app)
        self.assertEqual(func_app.app_service_config.linux_fx_version, '')
        self.assertEqual(func_app.app_service_config.java_version, '11')

    @context(module_path="language_version/functionapp_win_java_isnot_latest")
    def test_functionapp_win_java_isnot_latest(self, ctx: AzureEnvironmentContext):
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2152fwj-functionapp')
        self.assertIsNotNone(func_app)
        self.assertEqual(func_app.app_service_config.linux_fx_version, '')
        self.assertEqual(func_app.app_service_config.java_version, '1.8')

        # ------------------- https only tests -------------------

    @context(module_path="https_only/https_only_set_to_true")
    def test_https_only_set_to_true(self, ctx: AzureEnvironmentContext):
        # app_service = self._get_app_service(ctx, 'cr2300-https-only-webapp')
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2312-https-only-functionapp')
        self.assertIsNotNone(func_app)
        self.assertEqual(func_app.https_only, True)

    @context(module_path="https_only/https_only_set_to_false")
    def test_https_only_set_to_false(self, ctx: AzureEnvironmentContext):
        # app_service = self._get_app_service(ctx, 'cr2300-https-only-webapp')
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2312-https-only-functionapp')
        self.assertIsNotNone(func_app)
        self.assertEqual(func_app.https_only, False)

    @context(module_path="https_only/https_only_is_missing")
    def test_https_only_set_is_missing(self, ctx: AzureEnvironmentContext):
        # app_service = self._get_app_service(ctx, 'cr2300-https-only-webapp')
        func_app: AzureFunctionApp = ctx.function_apps.get('cr2312-https-only-functionapp')
        self.assertIsNotNone(func_app)
        self.assertEqual(func_app.https_only, False)
