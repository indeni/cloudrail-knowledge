from typing import List

from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.resources.ssm.ssm_parameter import SsmParameter
from test.knowledge.context.aws_context_test import AwsContextTest
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestSsmParameter(AwsContextTest):

    def get_component(self):
        return 'ssm/ssm_parameter'

    @context(module_path="default_encryption")
    def test_default_encryption(self, ctx: AwsEnvironmentContext):
        ssmp = self._ssm_parameter_analysis(ctx.ssm_parameters)
        self.assertEqual(ssmp.kms_data.key_manager, KeyManager.AWS)
        self.assertEqual(ssmp.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/systems-manager/parameters/test-cloudrail/description?region=us-east-1&tab=Table')

    def _ssm_parameter_analysis(self, ssm_param_resources: List[SsmParameter]):
        ssmp = next((ssmp for ssmp in ssm_param_resources if ssmp.name == 'test-cloudrail'), None)
        self.assertIsNotNone(ssmp)
        self.assertEqual(ssmp.ssm_type, 'SecureString')
        self.assertTrue(ssmp.kms_key_id)
        return ssmp

    @context(module_path="encrypted_aws_managed_key_arn")
    def test_encrypted_aws_managed_key_arn(self, ctx: AwsEnvironmentContext):
        ssmp = self._ssm_parameter_analysis(ctx.ssm_parameters)
        self.assertEqual(ssmp.kms_data.key_manager, KeyManager.AWS)

    @context(module_path="encrypted_customer_kms_creating")
    def test_encrypted_customer_kms_creating(self, ctx: AwsEnvironmentContext):
        ssmp = self._ssm_parameter_analysis(ctx.ssm_parameters)
        self.assertEqual(ssmp.kms_data.key_manager, KeyManager.CUSTOMER)

    @context(module_path="encrypted_customer_kms_existing_key", base_scanner_data_for_iac='account-data-ssm-param-kms-keys',
             test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_encrypted_customer_kms_existing_key(self, ctx: AwsEnvironmentContext):
        ssmp = self._ssm_parameter_analysis(ctx.ssm_parameters)
        self.assertEqual(ssmp.kms_data.key_manager, KeyManager.CUSTOMER)
