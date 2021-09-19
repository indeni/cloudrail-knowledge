from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestSageMakerNotebookInstance(AwsContextTest):

    def get_component(self):
        return "sagemaker"

    @context(module_path="sagemaker_notebook_instance_aws_managed_encrypted")
    def test_sagemaker_notebook_instance_encrypted_aws(self, ctx: AwsEnvironmentContext):
        sagemaker_notebook_instance = next((instance for instance in ctx.sagemaker_notebook_instances
                                            if instance.name == 'my-notebook-instance'), None)
        self.assertIsNotNone(sagemaker_notebook_instance)
        self.assertTrue(sagemaker_notebook_instance.arn)
        self.assertEqual(sagemaker_notebook_instance.kms_data.key_manager, KeyManager.AWS)
        self.assertEqual(sagemaker_notebook_instance.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/notebook-instances/my-notebook-instance')
        self.assertTrue(sagemaker_notebook_instance.direct_internet_access)

    @context(module_path="sagemaker_notebook_instance_data_encrypted_at_rest_with_customer_managed_key")
    def test_sagemaker_notebook_instance_encrypted_cmk(self, ctx: AwsEnvironmentContext):
        sagemaker_notebook_instance = next((instance for instance in ctx.sagemaker_notebook_instances
                                            if instance.name == 'my-notebook-instance'), None)
        self.assertIsNotNone(sagemaker_notebook_instance)
        self.assertTrue(sagemaker_notebook_instance.arn)
        self.assertEqual(sagemaker_notebook_instance.kms_data.key_manager, KeyManager.CUSTOMER)

    @context(module_path="no_public_access_sagemaker")
    def test_no_public_access_sagemaker(self, ctx: AwsEnvironmentContext):
        sagemaker_notebook_instance = next((instance for instance in ctx.sagemaker_notebook_instances
                                            if instance.name == 'my-notebook-instance'), None)
        self.assertFalse(sagemaker_notebook_instance.direct_internet_access)
