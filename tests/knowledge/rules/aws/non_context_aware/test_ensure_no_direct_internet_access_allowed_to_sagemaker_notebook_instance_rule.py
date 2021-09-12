import unittest

from cloudrail.knowledge.context.aws.resources.sagemaker.sagemaker_notebook_instance import SageMakerNotebookInstance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_no_direct_internet_access_allowed_to_sagemaker_notebook_instance_rule import \
    EnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule()

    def test_non_car_no_direct_internet_access_allowed_from_sagemaker_notebook_instance_rule_fail(self):
        # Arrange
        sagemaker_instance: SageMakerNotebookInstance = create_empty_entity(SageMakerNotebookInstance)
        sagemaker_instance.direct_internet_access = True
        context = AwsEnvironmentContext(sagemaker_notebook_instances=[sagemaker_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_no_direct_internet_access_allowed_from_sagemaker_notebook_instance_rule_pass(self):
        # Arrange
        sagemaker_instance: SageMakerNotebookInstance = create_empty_entity(SageMakerNotebookInstance)
        sagemaker_instance.direct_internet_access = False
        context = AwsEnvironmentContext(sagemaker_notebook_instances=[sagemaker_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
