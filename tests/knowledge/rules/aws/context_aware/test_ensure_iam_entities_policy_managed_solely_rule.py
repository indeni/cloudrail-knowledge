# Alon comment - rule have a lot of logic
# import unittest
#
# from cloudrail.knowledge.context.environment_context import AwsEnvironmentContext
# from cloudrail.knowledge.rules.aws.context_aware.ensure_iam_entities_policy_managed_solely_rule import EnsureIamEntitiesPolicyManagedSolely
# from cloudrail.knowledge.rules.base_rule import RuleResultType
# from cloudrail.dev_tools.rule_test_utils import create_empty_entity
#
#
# class TestEnsureIamEntitiesPolicyManagedSolely(unittest.TestCase):
#     def setUp(self):
#         self.rule = EnsureIamEntitiesPolicyManagedSolely()
#
#     def test_car_iam_policy_control_in_iac_only_fail(self):
#         # Arrange
#         context = AwsEnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_car_iam_policy_control_in_iac_only_pass(self):
#         # Arrange
#         context = AwsEnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
